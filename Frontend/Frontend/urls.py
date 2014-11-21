from django.conf.urls import patterns, include, url
from django.contrib import admin
import sys
import os

# path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'src'))
# os.chdir(path)
# sys.path.append(path)

# import executer
# executer.run("article")

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Frontend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^articles/', include('articles.urls')),

    url(r'^explorer/', include('explorer.urls')),

    url(r'^statistics/', include('statistics.urls')),

    url(r'^visualizations/', include('visualizations.urls')),

    url(r'^admin/', include(admin.site.urls)),
)


