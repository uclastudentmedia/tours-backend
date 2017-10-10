from __future__ import unicode_literals
from django.dispatch import receiver
from photologue.models import Gallery
from indoor.models import Building
from django.db import models
from sortedm2m.fields import SortedManyToManyField
from jsonfield import JSONField
from collections import OrderedDict

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Landmark(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat=models.FloatField(default=0)
    long=models.FloatField(default=0)
    text_description = models.TextField(null=True, blank=True, default="")
    category = models.ForeignKey(Category, null=True, blank=True, default=None)
    priority = models.IntegerField(default=1)
    gallery = models.OneToOneField(Gallery, blank=True, null=True, default=None)
    attributes = JSONField(null=True, blank=True, default=None,
            load_kwargs={'object_pairs_hook': OrderedDict})
    building = models.OneToOneField(Building, blank=True, null=True,
                                    default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Tour(models.Model):
    name=models.CharField(max_length=200, unique=True)
    landmarks=SortedManyToManyField(Landmark, verbose_name="list of landmarks")
    distance=models.FloatField()
    duration=models.IntegerField()
    text_description=models.TextField(null=True, blank=True, default="")
    icon=models.CharField(max_length=100, blank=True, default=None, null=True)
    image=models.ImageField(upload_to="tour/", null=True)

    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=Landmark)
def create_gallery(sender, instance, created, **kwargs):
    if created:
        instance.gallery = Gallery.objects.create(title=instance.name,
                                                  slug=str(instance.id))
        instance.save()

@receiver(models.signals.post_delete, sender=Landmark)
def delete_gallery(sender, instance, **kwargs):
    if instance.gallery:
        instance.gallery.delete()
