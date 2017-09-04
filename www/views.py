from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
from indoor import data
import json

def index(request):
    context = data.building_list_data()
    context = {
            "building_list_arr": json.dumps(context["results"])
            }
    return render(request, 'www/index.html', context)
