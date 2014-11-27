from django.conf.urls import patterns, url

from tweets import views

urlpatterns = patterns('',
    url(r'^getJson', views.getJson, name='getJson'),
    url(r'^warc/(?P<filename>.+)$', views.getWarc, name='getWarc'),
)