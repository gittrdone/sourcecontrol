from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^charts/', include('charting.urls')),
    url(r'^authors/', include('user_detail.urls')),
    url(r'^', include('reporting.urls')),
    url(r'^', include('sourceControlApp.urls')),
)
