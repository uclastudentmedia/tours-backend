from django.contrib import admin

from .models import Category, Landmark

# Register your models here.

admin.site.register(Landmark)
admin.site.register(Category)
