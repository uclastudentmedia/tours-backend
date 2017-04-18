from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site

from photologue.admin import GalleryAdmin
from photologue.models import Gallery

from .models import Category, Landmark

# Register your models here.

class LandmarkAdminForm(forms.ModelForm):
    class Meta:
        model = Landmark
        # The gallery is created automatically
        exclude = ['gallery']


@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    form = LandmarkAdminForm


admin.site.register(Category)


# Photologue

#admin.site.unregister(Gallery)
#admin.site.unregister(Site)
