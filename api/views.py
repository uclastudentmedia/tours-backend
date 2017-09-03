from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.forms.models import model_to_dict
from django.conf import settings
import os.path

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


# Caching landmarks
LANDMARKS_CACHE = [_get_landmark_detail(l) for l in Landmark.objects.all()]

def get_landmark_list():
    return LANDMARKS_CACHE

def get_landmark_detail(id):
    try:
        return filter(lambda l: l['id'] == int(id), LANDMARKS_CACHE)[0]
    except IndexError:
        raise Http404('No such landmark id=' + id)


def landmark_list(request):
    cached_filename = os.path.join(settings.MEDIA_ROOT, 'landmark/cache/landmark.json')
    try:
        with open(cached_filename) as cached_file:
            print "reading cached file " + cached_filename
            json_data = cached_file.read()
            return HttpResponse(json_data, content_type="application/json")
    except IOError as err:
        print err, ", using other cached data"
        landmarks = get_landmark_list()
        return JsonResponse({ "results": landmarks })


def landmark_detail(request, id):
    landmark = get_landmark_detail(id)
    return JsonResponse({ "results": landmark })


def category_list(request):
    categories = Category.objects.values('id',
                                        'name',
                                        'sort_order')
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
