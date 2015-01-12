# -*- coding: utf-8 -*-
import json
import re

from scrapy.contrib.spiders.crawl import CrawlSpider
from scrapy.http.request import Request

from bs4 import BeautifulSoup

from rankingspider.items import StatsItem
from rankingspider.mappings import get_all_schedules, get_schedule_by_id
from rankingspider.utils import strip_rank


class StatsSpider(CrawlSpider):
    name = 'statsspider'
    stats_categories = ['stats', 'efficiency', 'splits']
    process_columns = {
        'stats': {'Value (rank)': strip_rank},
        'efficiency': {},
        'splits': {}
    }

    def __init__(self, schedule=None, *args, **kwargs):
        self.schedule = schedule
        super(StatsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if self.schedule:
            schedule = get_schedule_by_id(self.schedule)
            for cat in self.stats_categories:
                request = Request('%s/%s'%(schedule.matchup_url, cat))
                request.meta['category'] = cat
                request.meta['schedule'] = schedule.id
                yield request
        else:
            for schedule in get_all_schedules():
                for cat in self.stats_categories:
                    request = Request('%s/%s'%(schedule.matchup_url, cat))
                    request.meta['category'] = cat
                    request.meta['schedule'] = schedule.id
                    yield request

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        data = []
        for module in soup.select('#content .module-in'):
            item = StatsItem()
            item['schedule'] = response.meta['schedule']
            item['category'] = response.meta['category']
            title = module.parent.h4.text
            head = []
            process_columns = {}
            for tr in module.select('thead tr'):
                ths = []
                for index, th in enumerate(tr.select('th')):
                    if th.text.strip() in self.process_columns[item['category']].keys():
                        processor = self.process_columns[item['category']][th.text.strip()]
                        process_columns[index] = processor
                        ths.append({'title': processor(th.text.strip()),
                                    'colspan': int(th.get('colspan', 1))})
                    else:
                        ths.append({'title': th.text.strip(),
                                    'colspan': int(th.get('colspan', 1))})
                head.append(ths)
            body = []
            for tr in module.select('tbody tr'):
                tds = []
                for index, td in enumerate(tr.select('td')):
                    text = td.text.strip()
                    if index not in process_columns.keys():
                        if not text:
                            # no text for this td. it should be special td.
                            if td.find(class_=re.compile('tr_arrowed')):
                                arrowed_el = td.find(class_=re.compile('tr_arrowed_\d'))
                                if arrowed_el:
                                    arrowed_level = int(re.match('tr_arrowed_(\d)', arrowed_el['class'][0]).group(1))
                                    # 1. adv column for stat splits
                                    if td.find(class_=re.compile('tr_arrowed_r')):
                                        tds.append(arrowed_level)
                                    elif td.find(class_=re.compile('tr_arrowed_l')):
                                        tds.append(arrowed_level*-1)
                                    else:
                                        raise Exception('Invalid class for adv column')
                                else:
                                    tds.append(0)
                        else:
                            tds.append(text)
                    else:
                        tds.append(process_columns[index](text))
                body.append(tds)
            data.append({'title': title, 'head': head, 'body': body})
        item['data'] = json.dumps(data)
        yield item
