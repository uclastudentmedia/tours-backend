from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic


def index(request):
    context = {}
    return render(request, 'index.html', context)
