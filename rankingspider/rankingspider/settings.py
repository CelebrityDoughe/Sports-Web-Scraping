# Scrapy settings for rankingspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'rankingspider'

SPIDER_MODULES = ['rankingspider.spiders']
NEWSPIDER_MODULE = 'rankingspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'rankingspider (+http://www.yourdomain.com)'

MYSQL_USERNAME = ''
MYSQL_PASSWORD = ''
MYSQL_DB_NAME = ''  # default charset should be utf-8
MYSQL_DB_HOST = '127.0.0.1'
MYSQL_DB_PORT = '3306'

ITEM_PIPELINES = [
    'rankingspider.pipelines.RankingspiderPipeline',
]

try:
    from local_settings import *  # noqa
except ImportError:
    pass
