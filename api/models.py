from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Landmark(models.Model):
    name = models.CharField(max_length=200)
    ctr_coord_lat=models.FloatField()
    ctr_coord_long=models.FloatField()
    # nw_coord_lat = models.FloatField()
    # nw_coord_long = models.FloatField()
    # se_coord_lat = models.FloatField()
    # se_coord_long = models.FloatField()
    text_description = models.TextField()

class Picture(models.Model):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)

class Audio(models.Model):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
