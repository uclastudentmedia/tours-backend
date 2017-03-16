import csv

from api.models import Landmark, Category

def import_landmarks(csv_filepath):
    with open(csv_filepath, 'r') as fd:
        #id,name,lat,long,text_description,category_id,category,norm_id
        dr = csv.DictReader(fd)

        landmarks = []
        for r in dr:
            if not r['category_id']:
                category = None
            else:
                category = Category.objects.get(id=r['category_id'])
            landmark = Landmark(id=r['norm_id'],
                                name=r['name'],
                                lat=r['lat'],
                                long=r['long'],
                                text_description=r['text_description'],
                                category=category)
            landmarks.append(landmark)
        Landmark.objects.bulk_create(landmarks)
