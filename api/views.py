from django.shortcuts import render
from django.views import generic

from .models import Landmark

def index(request):
    context = {}
    return render(request, 'api/index.html', context)

class LandmarkListView(generic.ListView):
    template_name = 'api/landmark_list.html'
    context_object_name = 'landmark_list'

    def get_queryset(self):
        return Landmark.objects.all()
