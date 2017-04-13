from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site

from photologue.admin import GalleryAdmin
from photologue.models import Gallery

from .models import Category, Landmark

# Register your models here.

admin.site.register(Landmark)
admin.site.register(Category)


# Photologue

#admin.site.unregister(Gallery)
#admin.site.unregister(Site)
