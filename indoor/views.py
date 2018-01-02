from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.forms.models import model_to_dict

from .models import Floor, Building, POI
from api.models import Landmark
from . import navigation, draw
from .data import building_list_data

from networkx import NetworkXNoPath, NetworkXError


def building_list_view(request):
    json_data = building_list_data()
    return JsonResponse(json_data)

def building_detail(request, landmark_id):
    try:
        landmark = Landmark.objects.get(id=int(landmark_id))
    except:
        raise Http404("Landmark does not exist.")
    if not landmark.building:
        raise Http404("Indoor navigation does not exist for this landmark.")

    floors = landmark.building.floor_set.all()
    pois = POI.objects.filter(floor__building=landmark.building)

    results = {}
    results['name'] = landmark.building.name
    results['landmark_id'] = landmark.id
    results['floors'] = [floor.name for floor in floors]
    results['pois'] = [poi.name for poi in pois]

    return JsonResponse({"results": results})     


def route(request, landmark_id, start_name, end_name):
    landmark_id = int(landmark_id)
    building = get_object_or_404(Building, landmark__id=landmark_id)

    if end_name == 'exit':
        try:
            end = POI.objects.filter(type='entrance', floor__building=building)[0]
            end_name = end.name
        except IndexError:
            raise Http404('Unable to find a route')

    try:
        paths,floors = navigation.route(building.name, start_name, end_name)
    except (POI.DoesNotExist, NetworkXNoPath, NetworkXError) as e:
        raise Http404('Unable to find a route')

    images = []
    for path, floor in zip(paths, floors):
        if not path:
            raise Exception("path is empty")
        draw.draw_route_image(landmark_id, floor, path, start_name, end_name)
        image_url = draw.get_route_image_url(landmark_id, floor,
                                             path[0], path[-1])
        images.append({
            'url': image_url,
            'floor': floor
        })

    return JsonResponse({
        'building': building.landmark.name,
        'landmark_id': landmark_id,
        'start': start_name,
        'end': end_name,
        'images': images
    })
