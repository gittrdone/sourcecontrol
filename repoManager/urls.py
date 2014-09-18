from django.conf.urls import patterns, url

from repoManager import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^count_files',views.count_files, name='count_files')
)