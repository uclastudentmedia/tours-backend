from .models import Building, Floor, RoomPolygon, POI, Path
import networkx as nx
import math

# TODO: save graphs in database when loading shapefiles

"""
Public exports:
get_floor
route
"""

# cost to use stairs
STAIR_COST = 10000

# floor difference to prefer elevator over stairs
ELEVATOR_THRESHOLD = 5

# cost to use elevators
ELEVATOR_COST = STAIR_COST * ELEVATOR_THRESHOLD


def get_floor(G):
    """
    @type G: nx.Graph
    @return: the floor that this graph is on
    @rtype: str
    """
    return G.floor


def set_floor(G, name):
    G.floor = name


def to_3d_coords(xy, floor_name):
    """
    create 3d coord tuples: (x, y, floor)
    """
    return (int(xy[0]), int(xy[1]), floor_name)


def generate_floor_graph(floor):
    """
    @type floor: Floor
    @rtype: nx.Graph

    The graph's nodes are represented as (x, y, floor)
    """

    G = nx.Graph()
    paths = Path.objects.filter(floor=floor)
    for path in paths:
        coords_seq = [to_3d_coords(xy, floor.name) for xy in path.geom.coords]

        # add nodes
        for coords in coords_seq:
            G.add_node(coords, name=str(coords))

        # add edges
        G.add_path(coords_seq)

    # rename nodes that are POIs
    pois = POI.objects.filter(floor=floor)
    for p in pois:
        coords_3d = to_3d_coords(p.geom.coords, floor.name)
        try:
            nx.set_node_attributes(G, 'name', {coords_3d: p.name})
        except KeyError: # this POI is not in the network, skip it
            # TODO: remove this exception, debugging only
            raise Exception("POI not connected to network: " + p.name)
            pass

    # set edge weights as distance
    for pt1, pt2 in G.edges_iter():
        distance = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
        G[pt1][pt2]['weight'] = distance
        G[pt1][pt2]['type'] = 'path'

    set_floor(G, floor.name)
    return G


def generate_building_graph(building):
    """
    @type building: Building
    @rtype: nx.Graph

    Combines the graphs of each floor with stairs/elevators
    """
    floors = Floor.objects.filter(building=building)
    floor_graphs = [generate_floor_graph(floor) for floor in floors]
    building_graph = nx.compose_all(floor_graphs)

    # add elevators to connect floors
    elevators = POI.objects.filter(type='elevator', floor__building=building)
    elevator_names = [p.name for p in elevators.distinct('name')]
    for elevator_name in elevator_names:
        points = elevators.filter(name=elevator_name)
        nodes = [to_3d_coords(p.geom.coords, p.floor.name) for p in points]

        # connect all elevator entrances to a dummy node
        dummy_node = 'dummy ' + elevator_name
        nodes = [dummy_node] + nodes

        # total cost of using elevators is weight * 2
        weight = ELEVATOR_COST / 2
        building_graph.add_star(nodes, weight=weight, type='elevator')

    # add stairs to connect floors
    stairs = POI.objects.filter(type='stair', floor__building=building)
    stair_names = [p.name for p in stairs.distinct('name')]
    for stair_name in stair_names:
        points = stairs.filter(name=stair_name).order_by('floor__level')
        nodes = [to_3d_coords(p.geom.coords, p.floor.name) for p in points]

        for i in range(len(nodes) - 1):
            # the cost to use stairs depends on the how many stories you go
            start_level = points[i].floor.level
            end_level = points[i+1].floor.level
            level_diff = end_level - start_level
            weight = STAIR_COST * level_diff

            start = nodes[i]
            end = nodes[i + 1]
            building_graph.add_edge(start, end, weight=weight, type='stair')

    # prevent further changes to the graph
    #nx.freeze(building_graph)

    return building_graph


def get_heuristic(building, use_stairs, use_elevators):
    """
    Creates a heuristic function based on whether stairs/elevators are used.
    """

    def level_diff(a, b):
        a_floor = Floor.objects.get(name=a[2], building=building)
        b_floor = Floor.objects.get(name=b[2], building=building)
        diff = abs(a_floor.level - b_floor.level)
        return diff

    if not use_stairs and not use_elevators:
        # no stairs or elevators are used, so can only be on the same floor
        def heuristic(a, b):
            return 0

    elif use_stairs and not use_elevators:
        # the cost of using level_diff flights of stairs
        def heuristic(a, b):
            return STAIR_COST * level_diff(a, b)

    elif not use_stairs and use_elevators:
        # the cost of using an elevator if the nodes are on different floors
        def heuristic(a, b):
            if type(a) is not tuple: # elevator dummy node
                return ELEVATOR_COST / 2
            if level_diff(a, b) == 0:
                return 0
            else:
                return ELEVATOR_COST

    elif use_stairs and use_elevators:
        # calculate the minimum cost of using stairs/elevators
        def heuristic(a, b):
            if type(a) is not tuple: # elevator dummy node
                return ELEVATOR_COST / 2
            diff = level_diff(a, b)
            if diff == 0:
                return 0
            else:
                stair_cost = STAIR_COST * diff
                elevator_cost = ELEVATOR_COST
                return min(stair_cost, elevator_cost)

    return heuristic


def route(building_name, start_name, end_name, use_stairs=True, use_elevators=False):
    """
    @type building_name: str
    @type start_name: str
    @type end_name: str
    @type use_stairs: bool
    @type use_elevators: bool
    @return: A tuple, (paths, floors). The best path from `start` to `end`.
             Each element is the part of the path on one floor. `floors`
             indicates which floor a particular `path` belongs to.
    @rtype: (list of list of (x,y) tuples, list of string)

    @throws: `model`.DoesNotExist, if building/start/end is not found
    @throws: nx.NetworkXNoPath, if no path is found
    @throws: nx.NetworkXError, if POI is not in graph

    eg: indoor.navigation.route('ackerman', '2400G', '2410')
    returns:
        (
          # paths
          [
            [
              (256, -601),
              (1042, -839),
            ],
            [
              (1214, -1262),
              (1267, -1113),
            ]
          ],

          # floors
          [
            u'2',
            u'b'
          ]
        )

    """

    # these must exist and be unique
    building = Building.objects.get(name=building_name)
    start = POI.objects.get(name=start_name, floor__building=building)
    end = POI.objects.get(name=end_name, floor__building=building)
    start_coords = to_3d_coords(start.geom.coords, start.floor.name)
    end_coords = to_3d_coords(end.geom.coords, end.floor.name)

    # get the routing network
    building_graph = generate_building_graph(building)

    # remove stairs/elevators from the graph if they are not used
    types = nx.get_edge_attributes(building_graph, 'type')
    if not use_stairs:
        stair_edges = [edge for edge in types if types[edge] == 'stair']
        building_graph.remove_edges_from(stair_edges)
    if not use_elevators:
        elevator_edges = [edge for edge in types if types[edge] == 'elevator']
        building_graph.remove_edges_from(elevator_edges)

    # do routing
    heuristic = get_heuristic(building, use_stairs, use_elevators)
    path = nx.astar_path(building_graph, start_coords, end_coords,
                         heuristic=heuristic, weight='weight')

    # separate path into floors
    separated_paths = []
    separated_paths.append([])

    for i in range(len(path) - 1):
        pt1 = path[i]
        pt2 = path[i+1]
        if building_graph[pt1][pt2]['type'] is 'path':
            # this edge is a path, add it to the current floor
            separated_paths[-1].append(path[i])
        else:
            # this edge is a stair/elevator, so there is a new floor
            separated_paths.append([])

    # add the last node to the last floor
    separated_paths[-1].append(path[-1])

    # filter out empty floors
    separated_paths = filter(lambda x: len(x) > 0, separated_paths)

    # get a list of the floor names
    floors = [floor[0][2] for floor in separated_paths]

    # change 3d coords back to 2d coords
    paths_2d = [[(x,y) for (x,y,z) in floor] for floor in separated_paths]

    return (paths_2d, floors)
