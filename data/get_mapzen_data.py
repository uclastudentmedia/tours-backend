import urllib, json, time
from api.models import Tour

def get_mapzen_data():
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
            api_key ="mapzen-kRYtVFg"
            url = "https://matrix.mapzen.com/optimized_route?json="+json.dumps(query) + "&api_key=" + "mapzen-kRYtVFg"	    
	    #construct url
	    #url = "https://tours.bruinmobile.com/optimized_route?json="+json.dumps(query)
	    print url
	    response = urllib.urlopen(url)
	    data = json.loads(response.read())
	    print data
	    #time and duration
	    tour.distance = data['trip']['summary']['length']
	    tour.duration = data['trip']['summary']['time']

	    tour.save()
	    time.sleep(5)
