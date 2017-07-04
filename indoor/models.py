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

class Point(models.Model):
    point_id = models.IntegerField()
    type = models.CharField(max_length=80)
    geom = models.PointField(srid=4326)

# Auto-generated `LayerMapping` dictionary for RoomPolygon model
point_mapping = {
    'point_id' : 'id',
    'type' : 'type',
    'geom' : 'POINT',
}
