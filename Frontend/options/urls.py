from django.conf.urls import patterns, url

from options import views

urlpatterns = patterns('',
    url(r'^downloads', views.downloads, name='downloads'),
    url(r'^downloads-excel', views.downloadsExcel, name='downloadsExcel'),
)
