import urllib, json
from api.models import Tour

tours = Tour.objects.all()
for tour in tours:
    landmarks = tour.landmarks.all()
    query = {}
    query["locations"] = list()
    for landmark in landmarks:
        coord={}
        coord["lat"] = landmark.lat
        coord["lon"] = landmark.long
        query["locations"].append(coord)

    query["costing"] = "pedestrian"
    query["directions_options"] = {}
    query["directions_options"]["units"] = "miles"
    
    #construct url
    url = "https://tours.bruinmobile.com/optimized_route?json="+json.dumps(query)
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    #time and duration
    tour.distance = data['trip']['summary']['length']
    tour.duration = data['trip']['summary']['time']

    #polyline
    data =  data["trip"]["locations"]
    print data
    for location in data:
        location.pop('original_index')
        location.pop('type')
        tour.polyline = data
    tour.save()
