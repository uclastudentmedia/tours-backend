from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.forms.models import model_to_dict

from .models import RoomPolygon, Floor, Building, POI
from api.models import Landmark
from . import navigation

from PIL import Image, ImageDraw, ImageFont
import os
import networkx as nx

def get_route_image_path(building_id, start_room, end_room):
    directory = "floor_plans/cache/"
    filename = str(building_id) + "_" + start_room + "_" + end_room + ".png"
    return os.path.join(settings.MEDIA_ROOT, directory, filename)

def get_floor_plan_path(building_id, floor_string):
    directory = "floor_plans/base/"
    filename = str(building_id) + "_" + floor_string + ".png"
    return os.path.join(settings.MEDIA_ROOT, directory, filename)

# Richard TODO: fix params and how they're used
def draw_route_image(building_id, floor, path, start, end):
    # TODO: probably clean up etc.
    image_path = get_floor_plan_path(building_name, floor)
    try:
        image = Image.open(image_path)
    except:
        raise Http404("Image " + newfilename + " does not exist or can't be opened")
    draw = ImageDraw.Draw(image)

    if start_room:
        # fill in rooms
        start_room_data = RoomPolygon.objects.get(name=start_room)
        start_border = start_room_data.geom.coords
        # room only has one polygon since we're using PolygonField
        start_border = [(n[0], -n[1]) for n in start_border[0]]
        draw.polygon(start_border, fill=(255, 114, 114, 255))
    if end_room:
        end_room_data = RoomPolygon.objects.get(name=end_room)
        end_border = end_room_data.geom.coords
        # room only has one polygon since we're using PolygonField
        end_border = [(n[0], -n[1]) for n in end_border[0]]
        draw.polygon(end_border, fill=(255, 114, 114, 255))

    # draw lines
    line_fill = (0, 113, 188, 255)
    #nodes, floors = route(building_name, start_room, end_room)
    #nodes = nodes[0]
    path = [(n[0], -n[1]) for n in path]
    for i in range(0, len(path)-1):
        draw.line((path[i], path[i+1]), fill=line_fill, width=18)

    # draw path
    rad = 10
    for (x,y) in path:
        draw.ellipse([x - rad, y - rad, x + rad, y + rad], fill=line_fill)

    # draw text centered in room
    font = ImageFont.truetype(os.path.join(settings.MEDIA_ROOT,
        "fonts/Roboto-Bold.ttf"), 40)
    if start_room:
        start_centroid = start_room_data.geom.centroid
        text_width, text_height = draw.textsize(start_room, font=font)
        start_coords = (start_centroid.x - text_width / 2,
                -start_centroid.y - text_height / 2)
        draw.text(start_coords, start_room, font=font, fill=(0, 188, 169, 255))
    if end_room:
        end_centroid = end_room_data.geom.centroid
        text_width, text_height = draw.textsize(end_room, font=font)
        end_coords = (end_centroid.x - text_width / 2,
                -end_centroid.y - text_height / 2)
        draw.text(end_coords, end_room, font=font, fill=(0, 188, 169, 255))

    # save modified image
    filename = get_image_filesys_path(building_id, start_room, end_room)
    image.save(filename, "PNG")

# Richard TODO: also fix these params
def get_image_url(building_id, floor, path, start_room, end_room):
    filename = get_image_filesys_path(building_id, start_room, end_room)
    if not os.path.isfile(filename):
        print "adding file to cache", newfilename
        draw_route_image_and_save(building_id, floor, start_room, end_room)
    else:
        print "read cached file", filename 
    # Richard TODO: return URL here

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
