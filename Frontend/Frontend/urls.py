from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import sys
import os

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Frontend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^articles/', include('articles.urls')),

    url(r'^tweets/', include('tweets.urls')),

    url(r'^explorer/', include('explorer.urls')),

    url(r'^statistics/', include('statistics.urls')),

    url(r'^visualizations/', include('visualizations.urls')),

    url(r'^options/', include('options.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^admin$', include(admin.site.urls)),

    # Home Page

    url(r'', include('home.urls')),

    url(r'^advanced_filters/', include('advanced_filters.urls'))
)

urlpatterns += staticfiles_urlpatterns()
