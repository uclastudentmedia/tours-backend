from .models import Floor, RoomPolygon, POI, Path
import networkx as nx
import math


# TODO: save graphs in database when loading shapefiles

def generate_graph(building, floor):
    f = Floor.objects.filter(building__name=building, name=floor).first()
    if f is None:
        raise Exception("Floor does not exist: " + building + ' ' + floor)

    net = nx.Graph()
    paths = Path.objects.filter(floor=f)
    for path in paths:
        coords = path.geom.coord_seq

        # add nodes
        for coord in coords:
            name = 'Node at ({x}, {y})'.format(x=int(coord[0]), y=int(coord[1]))
            net.add_node(coord, name=name)

        # add edges
        net.add_path(coords)

    # rename nodes that are POIs
    pois = POI.objects.filter(floor=f)
    for p in pois:
        try:
            nx.set_node_attributes(net, 'name', {p.geom.coords: p.name})
        except KeyError: # this POI is not in the network, skip it
            pass

    # set edge weights as distance
    for pt1, pt2 in net.edges_iter():
        distance = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
        net[pt1][pt2]['weight'] = distance

    return net
