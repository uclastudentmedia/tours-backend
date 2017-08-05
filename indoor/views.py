from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.forms.models import model_to_dict

from .models import Floor, Building, POI
from api.models import Landmark
from . import navigation, draw

from networkx import NetworkXNoPath, NetworkXError


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
    except (POI.DoesNotExist, NetworkXNoPath, NetworkXError) as e:
        raise Http404(e)

    image_urls = []
    for path, floor in zip(paths, floors):
        if not path:
            raise Exception("path is empty")
        draw.draw_route_image(landmark_id, floor, path, start_name, end_name)
        image_url = draw.get_route_image_url(landmark_id, floor,
                                             path[0], path[-1])
        image_urls.append(image_url)

    return JsonResponse({
        'building': building.name,
        'landmark_id': landmark_id,
        'start': start_name,
        'end': end_name,
        'images': image_urls
    })
