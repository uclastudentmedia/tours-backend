from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from indoor import data
from indoor.models import Building, POI
import json

def index(request):
    context_data = data.building_list_data()["results"]
    for building in context_data:
        building_obj = Building.objects.get(landmark__id=building["landmark_id"])
    building_list_dict = {building["name"]: building for building in context_data}
    context = {
            "building_list_dict": building_list_dict,
            "building_list_json": json.dumps(building_list_dict)
            }
    return render(request, 'www/index.html', context)
