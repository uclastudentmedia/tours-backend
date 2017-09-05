from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from indoor import data
import json

def index(request):
    context_data = data.building_list_data()["results"]
    context = {building["name"]: building for building in context_data}
    #context = dict(map(lambda building: { building["name"]: building }, context_data))
    context = {
            "building_list_dict": json.dumps(context)
            }
    return render(request, 'www/index.html', context)
