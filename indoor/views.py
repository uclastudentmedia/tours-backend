from django.shortcuts import render
from django.http import HttpResponse, Http404
#from api.models import Landmark
from PIL import Image
import magic
import random

INK = "red", "blue", "green", "yellow"

def generate_image(landmark_id, start, end):
    image = Image.new("RGB", (800, 600), random.choice(INK))
    return image

def get_floor_plan_image(building_name, floor_string):
    try:
        filename = "../assets/img/floor_plans/" + building_name + "_" + floor_string + ".png"
        img = Image.open(filename)
    except:
        raise Http404("Image " + filename + " does not exist or can't be opened")
    return img

def navigation_route(request, building_name, floor):
    """
    try:
        landmark = Landmark.objects.get(id=int(landmark_id))
    except:
        raise Http404("Landmark does not exist")
    image=generate_image(landmark_id, start, end)
    """
    image = get_floor_plan_image(building_name, floor)
    response=HttpResponse(image,content_type="image/png")
    image.save(response, "PNG")
    return response
