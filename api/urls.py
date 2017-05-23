from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^landmark/$', views.landmark_list, name='landmark'),
    url(r'^landmark/(?P<id>[0-9]+)/$', views.landmark_detail),
    url(r'^category/$', views.category_list, name='category'),
    url(r'^tour/$', views.tour_list, name='tour'),
    url(r'^tour/(?P<id>[0-9]+)/$', views.tour_detail),
]
