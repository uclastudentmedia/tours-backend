from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse

from .models import Landmark

def index(request):
    context = {}
    return render(request, 'api/index.html', context)

def landmark_list(request):
    landmarks = Landmark.objects.values('id',
                                        'name',
                                        'ctr_coord_lat',
                                        'ctr_coord_long')
    return JsonResponse({
        "results": list(landmarks)
    })
