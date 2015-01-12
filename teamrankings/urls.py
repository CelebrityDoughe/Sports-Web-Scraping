# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/teams/', permanent=False)),
    url(r'^teams/', include('teams.urls', namespace='teams', app_name='teams')),
    url(r'^schedules/', include('schedules.urls', namespace='schedules', app_name='schedules')),
    url(r'^stats/', include('stats.urls', namespace='stats', app_name='stats')),

    url(r'^admin/', include(admin.site.urls)),
)
