from django.conf.urls import url
from . import views

app_name='indoor'
urlpatterns=[
	#url(r'^indoor-nav/(?P<landmark_id>[0-9]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)$', views.navigation_route),
	url(r'^(?P<building_name>\w+)/(?P<floor>\w+)/(?P<start_room>\w+)/(?P<end_room>\w+)$', views.navigation_route),
        url(r'^(?P<landmark_id>[0-9]+)/(?P<start_room>\w+)/(?P<end_room>\w+)/(?P<start_end>[0-1])$', views.navigation_image),
]
