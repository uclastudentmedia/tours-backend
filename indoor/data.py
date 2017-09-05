from .models import Building, POI

def building_list_data():
    buildings_list = []
    for building in Building.objects.all():
        building_json = {}
        landmark_id = building.landmark.id
        floors = building.floor_set.all()
        pois = POI.objects.filter(floor__building=building)

        building_json['name'] = building.landmark.name
        building_json['landmark_id'] = landmark_id
        building_json['floors'] = [floor.name for floor in floors]
        building_json['pois'] = [poi.name for poi in pois]

        buildings_list.append(building_json)
    return {"results": buildings_list}
