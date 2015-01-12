# -*- coding: utf-8 -*-
import json

from django.db import models

from schedules.models import Schedule


class Stats(models.Model):

    CATEGORY_CHOICES = (
        ('stats', 'Matchup Stats'),
        ('efficiency', 'Efficiency Stats'),
        ('splits', 'Stat Splits'),
    )

    schedule = models.ForeignKey(Schedule)
    category = models.CharField(max_length=32, db_index=True,
                                choices=CATEGORY_CHOICES)
    data = models.TextField()

    @property
    def data_json(self):
        return json.loads(self.data)
