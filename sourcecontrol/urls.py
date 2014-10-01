from django.conf.urls import patterns, include, url
from django.contrib import admin

import sourceControlApp

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sourcecontrol.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('sourceControlApp.urls')),
)
