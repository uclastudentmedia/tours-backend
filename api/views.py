from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.forms.models import model_to_dict

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


def landmark_detail(request, id):
    landmark = model_to_dict(Landmark.objects.get(id=int(id)))
    
    return JsonResponse({ "results": landmark })
