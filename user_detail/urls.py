from django.conf.urls import patterns, url

from user_detail import views

urlpatterns = patterns('',
    url(r'^detail/(?P<cid>[0-9]+)', views.user_repo_detail, name='user_detail'),

)