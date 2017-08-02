from django.conf.urls import url
from . import views

app_name='indoor'
urlpatterns=[
    url(r'^route/(?P<landmark_id>\d+)/(?P<start>\w+)/(?P<end>\w+)$', views.route),
    url(r'^building$', views.building_list),
    url(r'^building/(?P<landmark_id>[0-9]+)$', views.building_detail),
]
