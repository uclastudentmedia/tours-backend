from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.admin import PhotoAdmin as PhotoAdminDefault
from photologue.models import Gallery, Photo

from .models import Category, Landmark, Tour

# api

class LandmarkAdminForm(forms.ModelForm):
    class Meta:
        model = Landmark
        exclude = ['gallery'] # the gallery is created automatically


@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    form = LandmarkAdminForm
    ordering = ('name',)
    search_fields = ['name', 'id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ['name', 'id']


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ['name', 'landmarks__name', 'landmarks__id']



# Photologue

admin.site.unregister(Gallery)
admin.site.unregister(Photo)
admin.site.unregister(Site)

@admin.register(Gallery)
class GalleryAdmin(GalleryAdminDefault):
    ordering = ('title',)
    search_fields = ['title', 'landmark__id']

@admin.register(Photo)
class PhotoAdmin(PhotoAdminDefault):
    ordering = ('title',)
    search_fields = ['title', 'galleries__title', 'galleries__landmark__id']
