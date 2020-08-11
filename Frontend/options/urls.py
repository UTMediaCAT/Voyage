from django.conf.urls import url

from options import views

urlpatterns = [
    url(r'^downloads/$', views.downloadPage, name="downloadPage"),
    url(r'^downloads/json', views.downloads, name='downloads'),
    url(r'^downloads/excel', views.downloadsExcel, name='downloadsExcel'),
    url(r'^downloads/twitterexcel', views.uploadExcelTwitter, name='uploadExcelTwitter')
]
