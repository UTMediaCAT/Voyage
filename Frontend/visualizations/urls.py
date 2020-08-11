from django.conf.urls import url

from visualizations import views

urlpatterns = [
    url(r'^$', views.not_available, name="not_available"),
]
