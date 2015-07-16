from django.conf.urls import patterns, url

from statistics import views

urlpatterns = patterns('',
	url(r'^articles_js', views.articles_js, name='articles_js'),
    url(r'^articles', views.articles, name='articles'),
    url(r'^tweets_js', views.tweets_js, name='tweets_js'),
    url(r'^tweets', views.tweets, name='tweets'),
)
