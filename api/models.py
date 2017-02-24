from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    sort_order = models.IntegerField()
    # the category's id within the app (not the database)
    category_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Landmark(models.Model):
    name = models.CharField(max_length=200)
    lat=models.FloatField()
    long=models.FloatField()
    text_description = models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

class Picture(models.Model):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)

class Audio(models.Model):
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
