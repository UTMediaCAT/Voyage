from django.conf.urls import patterns, url

from visualizations import views

urlpatterns = patterns('',
    url(r'^$', views.coming_soon_Visuals, name='Coming_Soon')
)
