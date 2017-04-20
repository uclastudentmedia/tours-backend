from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import Http404
from django.db.models import F

from .models import Landmark, Category
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
