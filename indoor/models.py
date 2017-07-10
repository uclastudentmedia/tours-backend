# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class Building(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Floor(models.Model):
    name = models.CharField(max_length=80)
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.building.__str__() + ' ' + self.name


class RoomPolygon(models.Model):
    name = models.CharField(max_length=80)
    geom = models.PolygonField(srid=4326)
    floor = models.ForeignKey(Floor, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.floor.__str__() + ' ' + self.name

# Auto-generated `LayerMapping` dictionary for RoomPolygon model
roompolygon_mapping = {
    'name' : 'name',
    'geom' : 'POLYGON',
}


class POI(models.Model):
    name = models.CharField(max_length=80)
    type = models.CharField(max_length=80)
    geom = models.PointField(srid=4326)
    floor = models.ForeignKey(Floor, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.floor.__str__() + ' ' + self.name

# Auto-generated `LayerMapping` dictionary for POI model
poi_mapping = {
    'name' : 'name',
    'type' : 'type',
    'geom' : 'POINT',
}


class Path(models.Model):
    path_id = models.IntegerField()
    geom = models.LineStringField(srid=4236)
    floor = models.ForeignKey(Floor, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.floor.__str__() + ' ' + str(self.id)

# Auto-generated `LayerMapping` dictionary for Path model
path_mapping = {
    'path_id' : 'id',
    'geom' : 'LINESTRING',
}
