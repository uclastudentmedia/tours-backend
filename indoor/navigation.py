from .models import Building, Floor, RoomPolygon, POI, Path
import networkx as nx
import math

# TODO: save graphs in database when loading shapefiles

"""
Public exports:
get_floor
route
"""


def get_floor(G):
    """
    @type G: networkx.Graph
    @return: the floor that this graph is on
    @rtype: str
    """
    return G.floor


def set_floor(G, name):
    G.floor = name


def generate_graph(floor):
    """
    @type floor: Floor
    @rtype: networkx.Graph
    """

    G = nx.Graph()
    paths = Path.objects.filter(floor=floor)
    for path in paths:
        coords = path.geom.coord_seq

        # add nodes
        for coord in coords:
            name = 'Node at ({x}, {y})'.format(x=int(coord[0]), y=int(coord[1]))
            G.add_node(coord, name=name)

        # add edges
        G.add_path(coords)

    # rename nodes that are POIs
    pois = POI.objects.filter(floor=floor)
    for p in pois:
        try:
            nx.set_node_attributes(G, 'name', {p.geom.coords: p.name})
        except KeyError: # this POI is not in the network, skip it
            pass

    # set edge weights as distance
    for pt1, pt2 in G.edges_iter():
        distance = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
        G[pt1][pt2]['weight'] = distance

    set_floor(G, floor.name)
    return G


def route(building_name, start_name, end_name):
    """
    @type building_name: str
    @type start_name: str
    @type end_name: str
    @return: The best path from `start` to `end`. Each element is the part of
             the path on one floor.
    @rtype: list of networkx.Graph

    eg: indoor.navigation.route('ackerman', '2400G', '2410')
    """

    # these must exist and be unique
    building = Building.objects.get(name=building_name)
    start = POI.objects.get(name=start_name, floor__building=building)
    end = POI.objects.get(name=end_name, floor__building=building)

    G = generate_graph(start.floor)

    try:
        path = nx.shortest_path(G, start.geom.coords, end.geom.coords, 'weight')
    except nx.NetworkXNoPath as e:
        print('no path found: ' + e.message)
        return [nx.null_graph()]

    # TODO: support multiple floors
    out = nx.Graph()
    out.add_path(path)
    set_floor(out, start.floor.name)

    return [out]
