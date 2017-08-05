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


# TODO: function to clear cache


def get_floor_plan_path(landmark_id, floor_name):
    directory = "floor_plans/base/"
    filename = str(landmark_id) + "_" + floor_name + ".png"
    return os.path.join(settings.MEDIA_ROOT, directory, filename)


def _get_route_image_relpath(landmark_id, floor_name, start_coords, end_coords):
    directory = "floor_plans/cache/"

    start_x, start_y = start_coords
    end_x, end_y = end_coords

    filename = "{id}_{floor}_{sx}-{sy}_{ex}-{ey}.png".format(
        id=landmark_id, floor=floor_name,
        sx=start_x, sy=(-start_y), ex=end_x, ey=(-end_y))

    return os.path.join(directory, filename)


def get_route_image_path(landmark_id, floor_name, start_coords, end_coords):
    relpath = _get_route_image_relpath(landmark_id, floor_name,
                                        start_coords, end_coords)
    return os.path.join(settings.MEDIA_ROOT, relpath)


def get_route_image_url(landmark_id, floor_name, start_coords, end_coords):
    relpath = _get_route_image_relpath(landmark_id, floor_name,
                                        start_coords, end_coords)
    return os.path.join(settings.MEDIA_URL, relpath)


def draw_route_image(landmark_id, floor_name, path, start_name, end_name):
    # TODO: probably clean up etc.

    # check if image is cached
    cache_image_path = get_route_image_path(landmark_id, floor_name,
                                            path[0], path[-1])
    if os.path.isfile(cache_image_path):
        # touch the cached file
        os.utime(cache_image_path, None)
        return

    # image is not cached, draw it

    building = Building.objects.get(landmark__id=landmark_id)
    floor = Floor.objects.get(name=floor_name, building=building)
    start = POI.objects.get(name=start_name, floor__building=building)
    end = POI.objects.get(name=end_name, floor__building=building)

    base_image_path = get_floor_plan_path(landmark_id, floor.name)
    try:
        image = Image.open(base_image_path)
    except:
        raise Http404("Image " + base_image_path + " does not exist or can't be opened")
    draw = ImageDraw.Draw(image)

    # fill in rooms
    if start.floor == floor:
        start_room_data = RoomPolygon.objects.get(name=start_name, floor=floor)
        start_border = start_room_data.geom.coords
        # room only has one polygon since we're using PolygonField
        start_border = [(n[0], -n[1]) for n in start_border[0]]
        draw.polygon(start_border, fill=(255, 114, 114, 255))
    if end.floor == floor:
        end_room_data = RoomPolygon.objects.get(name=end_name, floor=floor)
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
    if start.floor == floor:
        start_centroid = start_room_data.geom.centroid
        text_width, text_height = draw.textsize(start_name, font=font)
        start_coords = (start_centroid.x - text_width / 2,
                -start_centroid.y - text_height / 2)
        draw.text(start_coords, start_name, font=font, fill=(0, 188, 169, 255))
    if end.floor == floor:
        end_centroid = end_room_data.geom.centroid
        text_width, text_height = draw.textsize(end_name, font=font)
        end_coords = (end_centroid.x - text_width / 2,
                -end_centroid.y - text_height / 2)
        draw.text(end_coords, end_name, font=font, fill=(0, 188, 169, 255))

    # save modified image
    image.save(cache_image_path, "PNG")


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


def route(request, landmark_id, start_name, end_name):
    landmark_id = int(landmark_id)
    building = get_object_or_404(Building, landmark__id=landmark_id)

    try:
        paths,floors = navigation.route(building.name, start_name, end_name)
    except (POI.DoesNotExist, nx.NetworkXNoPath, nx.NetworkXError) as e:
        raise Http404(e)

    image_urls = []
    for path, floor in zip(paths, floors):
        if not path:
            raise Exception("path is empty")
        draw_route_image(landmark_id, floor, path, start_name, end_name)
        image_url = get_route_image_url(landmark_id, floor,
                                        path[0], path[-1])
        image_urls.append(image_url)

    return JsonResponse({
        'building': building.name,
        'landmark_id': landmark_id,
        'start': start_name,
        'end': end_name,
        'images': image_urls
    })
