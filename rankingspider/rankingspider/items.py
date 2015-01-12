# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
from scrapy.item import Item, Field


class TeamItem(Item):
    url = Field()
    name = Field()


class ScheduleItem(Item):
    team = Field()
    opponent = Field()
    date = Field()
    matchup_url = Field()
    location = Field()
    score = Field()
    opponent_score = Field()
    score_result = Field()
    result = Field()
    status = Field()


class StatsItem(Item):
    schedule = Field()
    category = Field()
    data = Field()
