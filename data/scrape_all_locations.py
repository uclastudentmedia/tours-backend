from api.models import Category, Landmark
from data.category_scraper import get_each_category
from data.landmark_scraper import get_landmark
from data.cat_id_scraper import get_location_from_cat

def scrape():
    Category.objects.all().delete()
    Landmark.objects.all().delete()

    categories = get_each_category()
    for category in categories:
        category.save()

    for category in categories:
        print("Category " + str(category.id))
        landmark_ids = get_location_from_cat(category.id)
        for landmark_id in landmark_ids:
            if not Landmark.objects.filter(id=landmark_id).exists():
                print("Landmark " + str(landmark_id))
                landmark = get_landmark(landmark_id)
                landmark.save()
