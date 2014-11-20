from django.conf.urls import patterns, url

from explorer import views

urlpatterns = patterns('',
    url(r'^$', views.command, name='command'),
    url(r'^getJson', views.getJson, name='getJson'),
)