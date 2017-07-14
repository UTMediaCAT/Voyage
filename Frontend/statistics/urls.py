from django.conf.urls import patterns, url

from statistics import views

urlpatterns = patterns('',
 	url(r'^$', views.not_available, name='not_available'),
)
