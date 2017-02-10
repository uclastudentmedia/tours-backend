import urllib2
import sys
from bs4 import BeautifulSoup
from api.models import Landmark

def get_page(location_id):
    # returns xml data from the endpoint for a location id
    endpoint = "http://space.admin.ucla.edu/locations_plsql/pkg_ucla.getlocation"
    url = endpoint + "?locid=" + str(location_id)
    #print "url:", url
    ret_xml = urllib2.urlopen(url).read()
    soup = BeautifulSoup(ret_xml, "lxml")
    return soup.location # all data is under a <location>

def get_data_for(location_id):
    # returns object for location id, None if error
    xml_data = get_page(location_id)
    if xml_data is None:
        print "No landmark data for ", location_id
        return None
    landmark_name = xml_data["map_name"]
    coordinates = xml_data.coordinates.find_all("coordinate")
    if len(coordinates) == 0:
        print "No coordinate data for ", location_id
        return None
    coordinates = coordinates[1]
    note = xml_data.note.string
    if note is None:
        note = "No description right now for this location."
    #print "name is", landmark_name
    #print "lat =", coordinates['y'], "long =", coordinates['x']
    #print "Note is: ", note 
    ret_obj = {
            "id": location_id,
            "name": landmark_name,
            "lat": coordinates['y'],
            "long": coordinates['x'],
            "note": note
    }
    print ret_obj
    return ret_obj

def main():
    Landmark.objects.all().delete()
    for id in range(1, 413):
        data = get_data_for(id)
        try:
            landmark = Landmark.objects.create(id=data['id'],
                                               name=data['name'],
                                               ctr_coord_lat=data['lat'],
                                               ctr_coord_long=data['long'],
                                               text_description=data['note'])
            landmark.save()
        except TypeError:
            pass

main()
