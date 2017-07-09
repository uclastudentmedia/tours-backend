from .models import Floor, RoomPolygon, POI, Path
import networkx as nx


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
            # TODO: set `name` to a POI name if available
            name = 'Node at ({x}, {y})'.format(x=int(coord[0]), y=int(coord[1]))
            net.add_node(coord, name=name)

        # add edges
        net.add_path(coords)

    # names = nx.get_node_attributes(net, 'name')
    return net
