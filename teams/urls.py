# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic.list import ListView

from .models import Team


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Team)),
)
