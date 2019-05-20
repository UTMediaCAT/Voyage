from django.conf.urls import patterns, url

from statistics import views

urlpatterns = patterns('',
	url(r'^$', views.comming_soon_statistics, name='statistics_comming'),
)
