from django.conf.urls import url
from . import views

app_name='images'
urlpatterns=[
	url(r'^landmark/(?P<id>[0-9]+)/(?P<number>[0-9]+)$', views.landmark_image),
]
