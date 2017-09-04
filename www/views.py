from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic
#from indoor import 


def index(request):
    context = {}
    return render(request, 'www/index.html', context)
