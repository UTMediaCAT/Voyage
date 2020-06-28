from django.conf.urls import patterns, url
from contactadmin import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^alert', views.alert, name='alert'),
)
