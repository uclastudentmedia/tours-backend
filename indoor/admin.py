from django.contrib.gis import admin
from .models import RoomPolygon, Point

# Register your models here.
admin.site.register(RoomPolygon, admin.GeoModelAdmin)
admin.site.register(Point, admin.GeoModelAdmin)

