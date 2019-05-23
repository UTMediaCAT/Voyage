from django.conf.urls import patterns, url

from visualizations import views

urlpatterns = patterns('',
    url(r'^$', views.coming_soon_visualizations, name='Coming Soon'),
)
