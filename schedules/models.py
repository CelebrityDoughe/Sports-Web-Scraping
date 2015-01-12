# -*- coding: utf-8 -*-
from django.db import models

from teams.models import Team


class Schedule(models.Model):
    """
    Schedule and result for the team
    """

    LOCATION_CHOICES = (
        ('home', 'Home'),
        ('away', 'Away'),
    )

    STATUS_CHOICES = (
        ('not started', 'Not started'),
        ('ended', 'Ended'),
    )

    team = models.ForeignKey(Team, related_name='schedules')
    opponent = models.ForeignKey(Team, related_name='opponent_schedules')
    date = models.DateField(db_index=True)
    matchup_url = models.URLField()
    location = models.CharField(max_length=16, choices=LOCATION_CHOICES)
    score = models.IntegerField(null=True, blank=True)
    opponent_score = models.IntegerField(null=True, blank=True)
    score_result = models.IntegerField(null=True, blank=True)
    result = models.CharField(max_length=32)
    status = models.CharField(max_length=16, db_index=True,
                              choices=STATUS_CHOICES)

    def __unicode__(self):
        return '[%s] (%s) VS (%s) [%s] --> %s' % (self.date, self.team,
                                                  self.opponent, self.location,
                                                  self.result)
