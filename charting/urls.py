from django.conf.urls import patterns, url

from charting import views

urlpatterns = patterns('',
    url(r'^user_detail_commits/(?P<committer_id>[0-9]+)', views.json_bar_data_for_user_repo_commits, name='user_repo_detail_bar_day'),
    url(r'^repo_detail/(?P<repo_id>[0-9]+)/(?P<branch_id>[0-9]+)', views.json_pie_data_for_repo, name='repo_detail_pie'),
    url(r'^repo_detail_day/(?P<repo_id>[0-9]+)/(?P<branch_id>[0-9]+)', views.json_bar_data_for_repo_commits, name='repo_detail_bar_day'),
)