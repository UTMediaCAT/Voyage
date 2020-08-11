from django.conf.urls import url

from explorer import views

urlpatterns = [
    url(r'^$', views.command, name='command'),
    url(r'^getJson', views.getJson, name='getJson'),
    url(r'^getDump', views.getDump, name='getDump'),
]