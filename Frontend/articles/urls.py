from django.conf.urls import patterns, url

from articles import views

urlpatterns = patterns('',
    url(r'^getJson', views.getJson, name='getJson'),
    url(r'^warc/(?P<filename>.+)$', views.getWarc, name='getWarc'),
    url(r'^pdf/(?P<filename>.+)$', views.getPDF, name='getPDF'),
    url(r'^img/(?P<filename>.+)$', views.getImg, name='getImg'),
)
