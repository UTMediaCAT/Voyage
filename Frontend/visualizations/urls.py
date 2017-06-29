from django.conf.urls import patterns, url

from visualizations import views

urlpatterns = patterns('',
    url(r'^$', views.not_available, name="not_available"),
 #    url(r'^article_hypertree$', views.article_hypertree, name='article_hypertree'),
 #    url(r'^article_hypertree_js$', views.article_hypertree_js, name='article_hypertree_js'),

 #    url(r'^article_spacetree$', views.article_spacetree, name='article_spacetree'),
 #    url(r'^article_spacetree_js$', views.article_spacetree_js, name='article_spacetree_js'),

 #    url(r'^article_weightedtree$', views.article_weightedtree, name='article_weightedtree'),
 #    url(r'^article_weightedtree_js$', views.article_weightedtree_js, name='article_weightedtree_js'),

	# url(r'^article_forcegraph$', views.article_forcegraph, name='article_forcegraph'),
 #    url(r'^article_forcegraph_js$', views.article_forcegraph_js, name='article_forcegraph_js'),

 #    url(r'^tweet_hypertree$', views.tweet_hypertree, name='tweet_hypertree'),
 #    url(r'^tweet_hypertree_js$', views.tweet_hypertree_js, name='tweet_hypertree_js'),

 #   	url(r'^tweet_spacetree$', views.tweet_spacetree, name='tweet_spacetree'),
 #    url(r'^tweet_spacetree_js$', views.tweet_spacetree_js, name='tweet_spacetree_js'),

 #    url(r'^tweet_weightedtree$', views.tweet_weightedtree, name='tweet_weightedtree'),
 #    url(r'^tweet_weightedtree_js$', views.tweet_weightedtree_js, name='tweet_weightedtree_js'),

	# url(r'^tweet_forcegraph$', views.tweet_forcegraph, name='tweet_forcegraph'),
 #    url(r'^tweet_forcegraph_js$', views.tweet_forcegraph_js, name='tweet_forcegraph_js'),
)
