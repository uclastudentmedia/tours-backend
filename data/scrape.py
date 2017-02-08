import urllib2
import sys
from bs4 import BeautifulSoup

def get_page(location_id):
    endpoint = "http://space.admin.ucla.edu/locations_plsql/pkg_ucla.getlocation"
    url = endpoint + "?locid=" + location_id
    print "url:", url
    ret_xml = urllib2.urlopen(url).read()
    soup = BeautifulSoup(ret_xml, "lxml")
    return soup.location # all data is under a <location>

def main():
    if (len(sys.argv) < 2):
        print "Usage: python scrape.py [LOCATION_ID]"
        return
    xml_data = get_page(sys.argv[1])
    landmark_name = xml_data["map_name"]
    coordinates = xml_data.coordinates.find_all("coordinate")[1]
    note = xml_data.note.string
    print "name is", landmark_name
    print "lat =", coordinates['y'], "long =", coordinates['x']
    print "Note is: ", note 

if __name__ == "__main__":
    main()
