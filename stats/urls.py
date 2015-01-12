# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import StatsDetailView


urlpatterns = patterns('',
    url(r'^$', StatsDetailView.as_view(), name='detail'),
)
