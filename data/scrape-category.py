from bs4 import BeautifulSoup
import urllib.request
import sys
from api.models import Category

# returns everyting inside the categories tag
def get_categories():
    url="http://space.admin.ucla.edu/locations_plsql/pkg_ucla.getlocationtypes"
    xml=urllib.request.urlopen(url).read()
    soup=BeautifulSoup(xml, "lxml")
    return soup.categories.contents 

#returns a list containing all the categories
def get_each_category():
    data=get_categories()
    categories=[]
    for item in data:
        obj=Category()
        obj.name=item["description"]
        obj.id=item["cat_id"]
        obj.sort_order=item["sortorder"]
        categories.append(obj)
    return categories    	

#tag=soup.title
#print(tag.name)
#print(tag.contents)`

def main():
    Category.objects.all().delete()
    data=get_each_category()
    for item in data:
        try:
            category = Category.objects.create(id=item.id, name=item.name, sort_order=item.sort_order)
            #category.save()
            print(category)
        except TypeError:
            pass

main()

