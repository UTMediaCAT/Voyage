from django.conf.urls import patterns, url

from statistics import views

urlpatterns = patterns('',
 	url(r'^$', views.notAvailable, name='not_available'),
)
