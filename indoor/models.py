# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class RoomPolygon(models.Model):
    name = models.CharField(max_length=80)
    geom = models.PolygonField(srid=4326)

# Auto-generated `LayerMapping` dictionary for indoor model
roompolygon_mapping = {
    'name' : 'name',
    'geom' : 'POLYGON',
}

class POI(models.Model):
    name = models.CharField(max_length=80)
    type = models.CharField(max_length=80)
    geom = models.PointField(srid=4326)

# Auto-generated `LayerMapping` dictionary for RoomPolygon model
poi_mapping = {
    'name' : 'name',
    'type' : 'type',
    'geom' : 'POINT',
}

class Path(models.Model):
    path_id = models.IntegerField()
    geom = models.LineStringField(srid=4236)

# Auto-generated `LayerMapping` dictionary for Path model
path_mapping = {
    'path_id' : 'id',
    'geom' : 'LINESTRING',
}
