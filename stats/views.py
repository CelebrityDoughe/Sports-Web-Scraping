# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView

from .models import Stats
from schedules.models import Schedule


class StatsDetailView(DetailView):
    model = Stats

    def get_object(self, queryset=None):
        schedule = Schedule.objects.get(pk=self.request.GET['schedule_id'])
        return Stats.objects.get(schedule=schedule, category=self.request.GET['category'])

    def get_context_data(self, **kwargs):
        data = super(StatsDetailView, self).get_context_data(**kwargs)
        schedule = Schedule.objects.get(pk=self.request.GET['schedule_id'])
        data.update({'schedule': schedule})
        return data
