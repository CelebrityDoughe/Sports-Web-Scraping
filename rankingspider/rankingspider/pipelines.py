# -*- coding: utf-8 -*-
import re

from rankingspider.items import TeamItem, ScheduleItem, StatsItem
from rankingspider.mappings import(
    Team, session, Schedule, Stats, get_team_by_url, get_schedule,
    get_stats
)


class RankingspiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, TeamItem):
            team = Team()
            if not get_team_by_url(item['url']):
                team.url = item['url']
                team.name = item['name']
                session.add(team)
                session.commit()
        elif isinstance(item, ScheduleItem):
            team_id = get_team_by_url(item['team']).id
            schedule = get_schedule(team_id, item['date'])
            if not schedule:
                schedule = Schedule()
                schedule.team = team_id
                schedule.date = item['date']
                schedule.matchup_url = item['matchup_url']
                schedule.location = item['location']
                schedule.opponent = get_team_by_url(item['opponent']).id
            schedule.result = item['result']
            matched = re.match('\w (\d*)-(\d*)', item['result'])
            if matched:
                schedule.status = 'ended'
                schedule.score = int(matched.group(1))
                schedule.opponent_score = int(matched.group(2))
                schedule.score_result = schedule.score-schedule.opponent_score
            else:
                schedule.status = 'not started'
            session.add(schedule)
            session.commit()
        elif isinstance(item, StatsItem):
            stats = get_stats(item['schedule'], item['category'])
            if not stats:
                stats = Stats()
                stats.schedule = item['schedule']
                stats.category = item['category']
            stats.data = item['data']
            session.add(stats)
            session.commit()

        return item
