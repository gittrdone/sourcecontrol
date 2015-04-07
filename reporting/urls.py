from django.conf.urls import patterns, url

from reporting import views

urlpatterns = patterns('',
    url(r'^repo/(?P<repo_id>[0-9]+)/reports/$', views.view_reports, name="reports"),
    url(r'^repo/(?P<repo_id>[0-9]+)/reports/(?P<report_id>[0-9]+)$', views.view_report, name="view_report"),
    url(r'^add_report/(?P<repo_id>[0-9]+)', views.add_report, name='add_report'),
    url(r'^edit_report/', views.edit_report, name='edit_report'),
    url(r'^delete_report/(?P<repo_id>[0-9]+)/(?P<report_id>[0-9]+)', views.delete_report, name='delete_report'),
    url(r'^repo/(?P<repo_id>[0-9]+)/reports/addReport', views.addReport, name='addReport'),
    url(r'^edit_query/', views.edit_query, name='edit_query'),
    url(r'^delete_query/(?P<repo_id>[0-9]+)/(?P<report_id>[0-9]+)/(?P<query_id>[0-9]+)', views.delete_query, name="delete_query")
)