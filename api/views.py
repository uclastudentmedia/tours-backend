from django.shortcuts import render
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

def landmark_list(request):
    queryset = Landmark.objects.annotate(category_id=F('category__category_id'))
    landmarks = queryset.values('id',
                                'name',
                                'lat',
                                'long',
                                'category_id',
                                'priority',
                                )
    return JsonResponse({
        "results": list(landmarks)
    })


def landmark_detail(request, id):
    try:
        landmark= Landmark.objects.get(id=int(id))
    except Landmark.DoesNotExist:
        raise Http404("Landmark does not exist")

    landmark_json = model_to_dict(landmark)
    landmark_json['image_count'] = landmark.gallery.photos.count()

    # remove extra spacing
    if landmark_json['attributes'] is None:
        landmark_json['attributes'] = '{}'
    else:
        attributes_json = json.loads(landmark_json['attributes'])
        landmark_json['attributes'] = json.dumps(attributes_json)

    del landmark_json['gallery']

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
    return JsonResponse({
	"results": tours_list
    })

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
