from django.conf.urls import url
from . import views

app_name='indoor'
urlpatterns=[
	url(r'^indoor-nav/(?P<landmark_id>[0-9]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)$', views.navigation_route),
]
