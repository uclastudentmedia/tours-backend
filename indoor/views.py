from django.shortcuts import render
from django.http import HttpResponse, Http404
from api.models import Landmark
from PIL import Image
import magic
import random

INK = "red", "blue", "green", "yellow"

def generate_image(landmark_id, start, end):
    image = Image.new("RGB", (800, 600), random.choice(INK))
    return image

def navigation_route(request, landmark_id, start, end):
    try:
        landmark = Landmark.objects.get(id=int(landmark_id))
    except:
        raise Http404("Landmark does not exist")
    image=generate_image(landmark_id, start, end)
    response=HttpResponse(image,content_type="image/png")
    image.save(response, "PNG")
    return response
