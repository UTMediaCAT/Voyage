from django.conf.urls import patterns, url

from visualizations import views

urlpatterns = patterns('',
    url(r'^article_hypertree$', views.article_hypertree, name='article_hypertree'),
    url(r'^article_hypertree_js$', views.article_hypertree_js, name='article_hypertree_js'),
    url(r'^article_spacetree$', views.article_spacetree, name='article_spacetree'),
    url(r'^article_spacetree_js$', views.article_spacetree_js, name='article_spacetree_js'),
    url(r'^tweet_hypertree$', views.tweet_hypertree, name='tweet_hypertree'),
    url(r'^tweet_hypertree_js$', views.tweet_hypertree_js, name='tweet_hypertree_js'),
)
