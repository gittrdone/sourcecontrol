from django.conf.urls import patterns, url

from reporting import views

urlpatterns = patterns('',
    url(r'^repo/(?P<repo_id>[0-9]+)/reports/', views.view_reports, name="reports"),
    url(r'^repo/(?P<repo_id>[0-9]+)/reports/(?P<report_id>[0-9]+)', views.view_report, name="view_report"),
    url(r'^repo/(?P<repo_id>[0-9]+)/reports/new/', views.new_report, name="new_report"),
    url(r'^add_report/', views.add_report, name='add_report'),
    url(r'^remove_report/', views.remove_report, name='remove_report')
)