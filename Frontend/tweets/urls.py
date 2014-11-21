from django.conf.urls import patterns, url

from tweets import views

urlpatterns = patterns('',
    url(r'^getJson', views.getJson, name='getJson'),
)