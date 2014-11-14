from django.conf.urls import patterns, url

from articles import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)