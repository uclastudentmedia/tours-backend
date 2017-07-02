import os
from django.core.files import File

from photologue.models import Gallery, Photo
from api.models import Landmark

def import_images(base_dir):
    """
    Imports images into the database. Assumes the images have paths of the
    form: '{base_dir}/{landmark_id}/images/{image_filename}'
    """

    for landmark_id in os.listdir(base_dir):
        try:
            landmark = Landmark.objects.get(id=int(landmark_id))
        except:
            continue

        photos_dir = os.path.join(base_dir, landmark_id, 'images')

        # add photos in numerical order
        for filename in sorted(os.listdir(photos_dir)):
            image_path = os.path.join(photos_dir, filename)
            no_ext = os.path.splitext(filename)[0]
            title = landmark_id + '_' + no_ext

            # create a Photo
            photo = Photo(title=title, slug=title)
            photo.image.save(title + '.jpg', File(open(image_path, 'r')))
            photo.save()

            # add the photo to the gallery
            landmark.gallery.photos.add(photo)
