from django.shortcuts import render
from django.http import HttpResponse, Http404
from api.models import Landmark

#import magic

def landmark_image(request, id, number):
    try:
        landmark=Landmark.objects.get(id=int(id))
    except Landmark.DoesNotExist:
        raise Http404("Landmark does not exist")
    photos= landmark.gallery.photos
    #n=int(number)+photos.first().id-1
    try:
        path=photos.all()[int(number)-1].image.path
    except IndexError:
        raise Http404("Photo does not exist")
    image=open(path, "rb").read()
    #image_type=magic.from_file(path, mime=True)
    #return Httpresponse(image, content_type=image_type)
    return HttpResponse(image, content_type="image/png")
