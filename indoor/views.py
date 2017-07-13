from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404
from api.models import Landmark
from .navigation import route
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import magic
import random
import os.path

INK = "red", "blue", "green", "yellow"

def generate_image():
    image = Image.new("RGB", (800, 600), random.choice(INK))
    return image

def get_floor_plan_image(building_name, floor_string):
    filename = "floor_plans/" + building_name.title() + "_" + floor_string + ".png"
    newfilename = os.path.join(settings.MEDIA_ROOT, filename)
    try:
        img = Image.open(newfilename)
    except:
        raise Http404("Image " + newfilename + " does not exist or can't be opened")
    return img

def navigation_route(request, building_name, floor, start_room, end_room):
    # TODO: probably clean up etc.
    image = get_floor_plan_image(building_name, floor)
    graph = route(building_name, start_room, end_room)[0]
    draw = ImageDraw.Draw(image)
    line_fill = (52, 152, 219, 255)
    for e in graph.edges():
        edgeList = [(e[0][0], -e[0][1]), (e[1][0], -e[1][1])]
        #print edgeList
        draw.line(edgeList, fill=line_fill, width=20)
    for n in graph.nodes():
        #print n
        x = n[0]
        y = -n[1]
        rad = 15
        draw.ellipse([x - rad, y - rad, x + rad, y + rad], fill=line_fill)
    response=HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response

def navigation_image(request, landmark_id, start_room, end_room, start_end):
    '''  
    try:
        landmark = Landmark.objects.get(id=int(landmark_id))
    except:
        raise Http404("Landmark does not exist")
    '''
    #start is 0
    if (start_end==0):
        image=generate_image(); #returns starting room highlighted and path drawn
    #end is 1
    else:
        image=generate_image(); #returns image with ending room highlighted
    response=HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response

