from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys


def get_location_from_cat(cat_id):
    url="http://space.admin.ucla.edu/locations_plsql/pkg_ucla.getlocationlist?cat_id="+ str(cat_id)
    #print(url)
    xml = urlopen(url).read()
    soup=BeautifulSoup(xml, "lxml")
    loc_ids=[]
    locations=soup.locations.contents 
    for location in locations:
        if location!='\n':
            #print(location)
            loc_ids.append(int(location["loc_id"]))
    return loc_ids

def main():
    loc_ids=[]
    loc_ids=get_location_from_cat(2)
    print(loc_ids)
