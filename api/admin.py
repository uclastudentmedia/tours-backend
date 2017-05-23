from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery

from .models import Category, Landmark, Tour

# Register your models here.

class LandmarkAdminForm(forms.ModelForm):
    class Meta:
        model = Landmark
        exclude = ['gallery'] # the gallery is created automatically


@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    form = LandmarkAdminForm
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)


# Photologue

admin.site.unregister(Gallery)
admin.site.unregister(Site)

@admin.register(Gallery)
class GalleryAdmin(GalleryAdminDefault):
    ordering = ('title',)

# Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    ordering = ('name',)
