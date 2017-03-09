from bs4 import BeautifulSoup
import urllib2
import sys
from api.models import Category

# returns everyting inside the categories tag
def get_categories():
    url="http://space.admin.ucla.edu/locations_plsql/pkg_ucla.getlocationtypes"
    xml = urllib2.urlopen(url).read()
    soup=BeautifulSoup(xml, "lxml")
    return soup.categories.contents 

#returns a list containing all the categories
def get_each_category():
    data=get_categories()
    categories=[]
    for item in data:
        print(item)
        categories.append(Category(name=item["description"],
                                   id=int(item["cat_id"]),
                                   category_id=int(item["cat_id"]) + 1000,
                                   sort_order=item["sortorder"]))
    return categories

#tag=soup.title
#print(tag.name)
#print(tag.contents)`

def main():
    Category.objects.all().delete()
    categories = get_each_category()
    for category in categories:
        try:
            category.save()
        except TypeError:
            pass
