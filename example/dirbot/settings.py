# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

ITEM_PIPELINES = {'dirbot.pipelines.FilterWordsPipeline': 1}

DOWNLOADER_MIDDLEWARES = {
  'scrapy_statsd_middleware.statsd_middleware.StatsdMiddleware': 543
}

SPIDER_MIDDLEWARES = {
  'scrapy_statsd_middleware.statsd_middleware.StatsdMiddleware': 543
}
