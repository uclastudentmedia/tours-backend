from django.contrib.gis.utils import LayerMapping
from .models import Building, Floor, RoomPolygon, POI, Path
from .models import roompolygon_mapping, poi_mapping, path_mapping
from api.models import Landmark
from .navigation import generate_building_graph
import os

INDOORS_GIS_ROOT = '/var/www/html/indoors-gis'

def get_shp_path(building, floor, type):
    filename = '-'.join([building, floor, type]) + '.shp'
    shp_path = os.path.join(INDOORS_GIS_ROOT, building, floor, filename)
    return shp_path


def load_rooms(building, floor, verbose=True):
    """
    eg. load_rooms('ackerman', '2')
    """
    rooms_shp = get_shp_path(building, floor, 'rooms')
    rooms_lm = LayerMapping(RoomPolygon, rooms_shp, roompolygon_mapping,
            transform=False,encoding='iso-8859-1')
    rooms_lm.save(strict=True, verbose=verbose)

def load_points(building, floor, verbose=True):
    points_shp = get_shp_path(building, floor, 'points')
    points_lm = LayerMapping(POI, points_shp, poi_mapping,
            transform=False,encoding='iso-8859-1')
    points_lm.save(strict=True, verbose=verbose)

def load_paths(building, floor, verbose=True):
    paths_shp = get_shp_path(building, floor, 'paths')
    paths_lm = LayerMapping(Path, paths_shp, path_mapping,
            transform=False,encoding='iso-8859-1')
    paths_lm.save(strict=True, verbose=verbose)


# holds all of the buildings to load
INDOOR_BUILDINGS = [
    {
        'name': 'ackerman',
        'floors': ['b', '2'],
        'landmark_id': 31,
    },
    {
        'name': 'boelter',
        'floors': ['4'],
        'landmark_id': 67,
    },
]

def load(delete=True, verbose=True, buildings=None):
    if delete:
        delete_gis_data()

    if not buildings:
        buildings = INDOOR_BUILDINGS

    for building_dict in buildings:
        building_name = building_dict['name']
        floors = building_dict['floors']
        landmark_id = building_dict['landmark_id']

        building = Building.objects.create(name=building_name)
        landmark = Landmark.objects.get(id=landmark_id)
        landmark.building = building
        landmark.save()

        for index, floor_name in enumerate(floors):
            floor = Floor.objects.create(name=floor_name,
                                         building=building,
                                         level=index)

            if verbose:
                print('Loading {b} {f}'.format(b=building, f=floor))

            try:
                load_rooms(building_name, floor_name, verbose)
                load_points(building_name, floor_name, verbose)
                load_paths(building_name, floor_name, verbose)
            except Exception as e:
                print('Failed to load {b} {f}'.format(b=building, f=floor))
                print(e.message)

            # Hacky way to set the floor foreign key:
            # Assume a feature belongs to the current floor if floor=None
            RoomPolygon.objects.filter(floor=None).update(floor=floor)
            POI.objects.filter(floor=None).update(floor=floor)
            Path.objects.filter(floor=None).update(floor=floor)

        building.graph = generate_building_graph(building)
        building.save()


def delete_gis_data():
    Building.objects.all().delete() # cascading delete
