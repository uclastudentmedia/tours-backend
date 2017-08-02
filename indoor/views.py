from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import RoomPolygon, Floor, Building, POI
from api.models import Landmark
from . import navigation
from PIL import Image, ImageDraw, ImageFont
from django.forms.models import model_to_dict
from django.http import JsonResponse

import matplotlib.pyplot as plt
import magic
import random
import os.path
import networkx as nx


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
    start_room_data = RoomPolygon.objects.get(name=start_room)
    end_room_data = RoomPolygon.objects.get(name=end_room)
    draw = ImageDraw.Draw(image)

    # fill in rooms
    start_border = start_room_data.geom.coords
    # room only has one polygon since we're using PolygonField
    start_border = [(n[0], -n[1]) for n in start_border[0]]
    draw.polygon(start_border, fill=(255, 114, 114, 255))
    end_border = end_room_data.geom.coords
    # room only has one polygon since we're using PolygonField
    end_border = [(n[0], -n[1]) for n in end_border[0]]
    draw.polygon(end_border, fill=(255, 114, 114, 255))

    # draw lines
    line_fill = (0, 113, 188, 255)
    nodes, floors = route(building_name, start_room, end_room)
    nodes = nodes[0]
    nodes = [(n[0], -n[1]) for n in nodes]
    for i in range(0, len(nodes)-1):
        draw.line((nodes[i], nodes[i+1]), fill=line_fill, width=18)

    # draw nodes
    rad = 10
    for (x,y) in nodes:
        draw.ellipse([x - rad, y - rad, x + rad, y + rad], fill=line_fill)

    # draw text centered in room
    font = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT,
        "fonts/Roboto-Bold.ttf"), 40)
    start_centroid = start_room_data.geom.centroid
    text_width, text_height = draw.textsize(start_room, font=font)
    start_coords = (start_centroid.x - text_width / 2,
            -start_centroid.y - text_height / 2)
    draw.text(start_coords, start_room, font=font, fill=(0, 188, 169, 255))
    end_centroid = end_room_data.geom.centroid
    text_width, text_height = draw.textsize(end_room, font=font)
    end_coords = (end_centroid.x - text_width / 2,
            -end_centroid.y - text_height / 2)
    draw.text(end_coords, end_room, font=font, fill=(0, 188, 169, 255))

    # return modified image
    response=HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response


def building_list(request):
    query_set = Building.objects.all()
    buildings = []
    for item in query_set:
        building = {}
        landmark_id = item.landmark.id
        floors = item.floor_set.all()
        building['name'] = item.name
        building['landmark_id'] = landmark_id
        building['floors'] = []
        for floor in floors:
            building['floors'].append(floor.name)
        buildings.append(building)
    return JsonResponse({"results": buildings})


def building_detail(request, landmark_id):
    try:
        landmark = Landmark.objects.get(id=int(landmark_id))
    except:
        raise Http404("Landmark does not exist.")
    if not landmark.building:
        raise Http404("Indoor navigation does not exist for this landmark.")
    results = {}
    results['name'] = landmark.building.name
    results['landmark_id'] = landmark.id
    floors = landmark.building.floor_set.all() 
    floor_poi = {}
    for floor in floors:
        POIs = floor.poi_set.all()
        poi_list = []
        for poi in POIs:
            poi_list.append(poi.name)
        floor_poi[floor.name] = poi_list
    results['pois'] = floor_poi
    return JsonResponse({"results": results})     


def route(request, landmark_id, start, end):

    landmark_id = int(landmark_id)
    building = get_object_or_404(Building, landmark__id=landmark_id)

    try:
        paths,floors = navigation.route(building.name, start, end)
    except (POI.DoesNotExist, nx.NetworkXNoPath, nx.NetworkXError) as e:
        raise Http404(e)

    image_urls = []
    for path, floor in zip(paths, floors):
        # TODO: integrate with image saving code
        # image_url = GETIMAGEURL(path, floor)
        # images_urls.append(image_url)
        image_urls.append("test.bruinmobile.com/" + floor)

    return JsonResponse({
        'building': building.name,
        'landmark_id': landmark_id,
        'start': start,
        'end': end,
        'images': image_urls
    })
