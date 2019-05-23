from django.conf.urls import patterns, url

from statistics import views

urlpatterns = patterns('',
    url(r'^$', views.coming_soon_statistics, name='Coming Soon'),
)
