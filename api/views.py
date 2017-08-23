from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import Http404
from django.db.models import F
import json

from .models import Landmark, Category, Tour

def index(request):
    context = {}
    return render(request, 'api/index.html', context)


def _get_landmark_detail(landmark):
    landmark_json = model_to_dict(landmark)

    try:
        landmark_json['category_id'] = landmark.category.id
    except AttributeError:
        landmark_json['category_id'] = None

    landmark_json['attributes'] = landmark.attributes

    landmark_json['indoor_nav'] = (landmark.building is not None)

    del landmark_json['gallery']

    landmark_json['images'] = [{
        'thumbnail': photo.get_thumbnail_url(),
        'display': photo.get_display_url(),
        'original': photo.image.url,
    } for photo in landmark.gallery.photos.all()]

    return landmark_json


def landmark_list(request):
    landmarks = [_get_landmark_detail(l) for l in Landmark.objects.all()]
    return JsonResponse({ "results": landmarks })


def landmark_detail(request, id):
    landmark = get_object_or_404(Landmark, id=int(id))
    landmark_json = _get_landmark_detail(landmark)
    return JsonResponse({ "results": landmark_json })


def category_list(request):
    categories = Category.objects.values('id',
                                        'name',
                                        'sort_order',
                                        'category_id')
    return JsonResponse({
        "results": list(categories)
    })

def tour_list(request):
    tours=list(Tour.objects.all())
    tours_list=[]
    for tour in tours:
        tour= model_to_dict(tour)
        tour['landmark_ids'] = list(tour['landmarks'].values('id'))
        tour['landmark_ids'] = [l["id"] for l in tour['landmark_ids']]
        del tour['landmarks']
        tours_list.append(tour)
    return JsonResponse({"results": tours_list})

def tour_detail(request, id):
    try:
        tour= Tour.objects.get(id=int(id))
    except Landmark.DoesNotExist:
        raise Http404("Tour does not exist")
    tour_json = model_to_dict(tour)
    tour_json['landmark_ids'] = list(tour_json['landmarks'].values('id')) 
    tour_json['landmark_ids']=[l["id"] for l in tour_json["landmark_ids"]]
    del tour_json['landmarks']
    return JsonResponse({"results": tour_json}) 
