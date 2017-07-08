from django.contrib.gis.utils import LayerMapping
from .models import RoomPolygon, POI, Path
from .models import roompolygon_mapping, poi_mapping, path_mapping
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


def load_floors(delete=False):
    buildings = {
        'ackerman': ['2'],
        #'boelter': ['4', '6'],
    }

    if delete:
        delete_gis_data()

    for building in buildings:
        for floor in buildings[building]:
            print('Loading {b} {f}'.format(b=building, f=floor))
            load_rooms(building, floor)
            load_points(building, floor)
            load_paths(building, floor)

def delete_gis_data():
    RoomPolygon.objects.all().delete()
    POI.objects.all().delete()
    Path.objects.all().delete()
