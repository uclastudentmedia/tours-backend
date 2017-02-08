from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^landmark/$', views.LandmarkListView.as_view(), name='landmark'),
]
