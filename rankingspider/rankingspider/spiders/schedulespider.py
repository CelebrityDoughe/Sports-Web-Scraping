# -*- coding: utf-8 -*-
import re
from urlparse import urljoin

from scrapy.contrib.spiders.crawl import CrawlSpider

from bs4 import BeautifulSoup

from rankingspider.items import ScheduleItem
from rankingspider.mappings import get_all_teams


class ScheduleSpider(CrawlSpider):
    name = 'schedulespider'
    team_url = 'http://www.teamrankings.com/ncaa-basketball/team/%s'

    def __init__(self, team=None, *args, **kwargs):
        if team:
            self.start_urls = [self.team_url%team]
        else:
            self.start_urls = [self.team_url%t.url for t in get_all_teams()]
        super(ScheduleSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        for tr in soup.select('#content-main .module-in tbody tr'):
            if tr.select('a'):
                # date is clickable
                item = ScheduleItem()
                item['date'] = re.match('.*\D-(\d*-\d*-\d*)', tr.select('a')[0]['href']).group(1)
                item['matchup_url'] = urljoin(response.url, tr.select('a')[0]['href'])
                item['team'] = re.match('.*/team/(.*)', response.url).group(1)
                item['opponent'] = re.match('.*/team/(.*)', tr.select('a')[1]['href']).group(1)
                item['location'] = tr.select('td')[3].text.lower()
                item['result'] = tr.select('td')[2].text
                yield item
