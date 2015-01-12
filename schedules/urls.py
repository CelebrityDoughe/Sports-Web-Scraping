# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import TeamScheduleListView

urlpatterns = patterns('',
    url(r'^$', TeamScheduleListView.as_view(), name='list'),
)
