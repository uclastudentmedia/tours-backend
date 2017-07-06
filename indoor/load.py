from django.contrib.gis.utils import LayerMapping
from .models import *

rooms_shp = "/var/www/html/indoors-gis/ackerman/2/ackerman-2-rooms.shp"
points_shp = "/var/www/html/indoors-gis/ackerman/2/ackerman-2-points.shp"
paths_shp = "/var/www/html/indoors-gis/ackerman/2/ackerman-2-paths.shp"

def run(verbose=True):
    rooms_lm = LayerMapping(RoomPolygon, rooms_shp, roompolygon_mapping,
            transform=False,encoding='iso-8859-1')
    rooms_lm.save(strict=True, verbose=verbose)
    points_lm = LayerMapping(Point, points_shp, point_mapping,
            transform=False,encoding='iso-8859-1')
    points_lm.save(strict=True, verbose=verbose)

def load_paths(verbose=True):
    paths_lm = LayerMapping(Path, paths_shp, path_mapping,
            transform=False,encoding='iso-8859-1')
    paths_lm.save(strict=True, verbose=verbose)
