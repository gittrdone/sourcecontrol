from django.conf.urls import patterns, url

from sourceControlApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^count_files',views.add_repo, name='count_files'),

    url(r'^edit_repo$',views.edit_repo, name='edit_repo'),
    url(r'^delete_repo/(?P<id>[0-9]+)',views.delete_repo, name='delete_repo'),

    url(r'^repo/detail/([0-9]+)/([0-9]+)', views.repo_detail, name='repo_detail'),
    url(r'^status/([0-9]+)', views.repo_status, name='repo_status'),

    url(r'^signup', views.signup, name='signup'),
    url(r'^do_signup', views.do_signup, name='do_signup'),

    url(r'^login', views.logon, name='login'),
    url(r'^do_login', views.do_logon, name='do_login'),

    url(r'^query/help', views.queryhelp, name='query_help'),
    url(r'^query/reference', views.queryref, name='query_ref'),
    url(r'^query/examples', views.queryexamples, name='query_example'),
    url(r'^edit_user_settings', views.edit_user_settings, name='edit_user_settings'),

    url(r'^logout', views.do_logout, name='logout'),
)