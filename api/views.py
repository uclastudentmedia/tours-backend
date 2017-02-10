from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import Http404

from .models import Landmark

def index(request):
    context = {}
    return render(request, 'api/index.html', context)

def landmark_list(request):
    landmarks = Landmark.objects.values('id',
                                        'name',
                                        'lat',
                                        'long')
    
    
    return JsonResponse({
        "results": list(landmarks)
    })


def landmark_detail(request, id):
    try:
        landmark= Landmark.objects.get(id=int(id))
    except Landmark.DoesNotExist:
        raise Http404("Landmark does not exist")
    return JsonResponse({ "results": model_to_dict(landmark) })
