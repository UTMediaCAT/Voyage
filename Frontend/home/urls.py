from django.conf.urls import patterns, url

from home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^services/', views.services, name='services'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^contact/', views.contact, name='contact'),
)
