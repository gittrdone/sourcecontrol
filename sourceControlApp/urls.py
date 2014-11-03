from django.conf.urls import patterns, url

from sourceControlApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^count_files',views.add_repo, name='count_files'),

    url(r'^repo_detail', views.repo_detail, name='repo_detail'),
    url(r'^status/([0-9]+)', views.repo_status, name='repo_status'),

    url(r'^signup', views.signup, name='signup'),
    url(r'^do_signup', views.do_signup, name='do_signup'),

    url(r'^login', views.logon, name='login'),
    url(r'^do_login', views.do_logon, name='do_login'),

    url(r'^logout', views.do_logout, name='logout'),
)