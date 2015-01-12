# -*- coding: utf-8 -*-
from django.views.generic.list import ListView

from .models import Schedule
from teams.models import Team


class TeamScheduleListView(ListView):
    model = Schedule

    def get_queryset(self):
        qs = super(TeamScheduleListView, self).get_queryset()
        return qs.filter(team=Team.objects.get(pk=self.request.GET['team_id']))

    def get_context_data(self, **kwargs):
        data = super(TeamScheduleListView, self).get_context_data(**kwargs)
        data.update({'team': Team.objects.get(pk=self.request.GET['team_id'])})
        return data
