from django.contrib.gis import admin
from .models import RoomPolygon, POI, Path

# Register your models here.
admin.site.register(RoomPolygon, admin.GeoModelAdmin)
admin.site.register(POI, admin.GeoModelAdmin)
admin.site.register(Path, admin.GeoModelAdmin)

