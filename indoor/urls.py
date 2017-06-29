from django.conf.urls import url
from . import views

app_name='images'
urlpatterns=[
	url(r'indoor-nav/(?P<id>[0-9]+)/(?P<start>[0-9]+/(?P<end>[0-9]+))$', views.route_image),
]
