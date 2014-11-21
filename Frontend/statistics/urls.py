from django.conf.urls import patterns, url

from statistics import views

urlpatterns = patterns('',
    url(r'^articles', views.articles, name='articles'),
    url(r'^tweets$', views.tweets, name='tweets'),
)
