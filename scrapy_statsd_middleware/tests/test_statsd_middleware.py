import socket
import unittest

from scrapy.http import Request, Response
from scrapy.spiders import Spider
from scrapy import Item
from statsd_middleware import StatsdMiddleware
from statsd_mock import udp_client, sock_check
# from scrapy.utils.test import get_crawler
from scrapy.crawler import CrawlerRunner

class Banana(Item): pass
class Apple(Item): pass
class Orange(Item): pass


class StatsdMiddlewareTest(unittest.TestCase):

  def setUp(self):
    crawler = CrawlerRunner().create_crawler(Spider)
    self.spider = crawler._create_spider('foo')
    self.mw = StatsdMiddleware().from_crawler(crawler)
    self.mw.spider_opened(self.spider)

    self.statsd_prefix = "{}.{}.".format(socket.gethostname(), self.spider.name)
    self.client = udp_client(self.statsd_prefix)
    self.mw.statsd_client = self.client

  def tearDown(self):
    del self.mw
    del self.client
    del self.spider
    del self.statsd_prefix

  def test_statsd_client(self):
    self.mw.statsd_client.incr('foo')
    sock_check(self.client._sock, 1, 'udp', val='{}.foo:1|c'.format(self.statsd_prefix))

  def test_process_request(self):
    req = Request('http://scrapytest.org/')
    self.mw.process_request(req, self.spider)
    sock_check(self.client._sock,
               1,
               'udp',
               val='{}.spider_reqs_issued:1|c'.format(self.statsd_prefix))

  def test_process_response(self):
    req = Request('http://scrapytest.org/')
    resp = Response('http://scrapytest.org/')
    self.mw.process_response(req, resp, self.spider)
    sock_check(self.client._sock,
               1,
               'udp',
               val='{}.spider_resps_received:1|c'.format(self.statsd_prefix))

  def test_process_exception(self):
    req = Request('http://scrapytest.org/')
    test_exception = KeyError()
    self.mw.process_exception(req, test_exception, self.spider)
    sock_check(self.client._sock,
               1,
               'udp',
               val='{}.error_KeyError:1|c'.format(self.statsd_prefix))

  def test_process_spider_exception(self):
    test_exception = IOError()
    resp = Response('http://scrapytest.org/')
    self.mw.process_exception(resp, test_exception, self.spider)
    sock_check(self.client._sock,
               1,
               'udp',
               val='{}.error_IOError:1|c'.format(self.statsd_prefix))

  def test_process_spider_output(self):
    results = [Banana(), Banana(), Apple(), Orange()]

    resp = Response('http://scrapytest.org/')
    client = udp_client(self.statsd_prefix)
    pipeline = client.pipeline()
    self.mw.statsd_client = pipeline
    self.mw.process_spider_output(resp, results, self.spider)
    pipeline.send()

    expected_val = "\n".join(map(lambda x: "{}.processed_{}:1|c".format(self.statsd_prefix,
                                                                        type(x).__name__), results))
    sock_check(client._sock,
               1,
               'udp',
               val=expected_val)

  def test_init_spider(self):
    self.assertEqual(self.mw.statsd_prefix, self.statsd_prefix)
    self.assertIsNotNone(self.mw.statsd_client)

  def test_init_spider_custom_name(self):
    hostname = 'captn-fluffington'
    spider_name = 'test-spider'
    prefix_pattern = '{hostname}_{name}_dev_'
    expected_prefix = prefix_pattern.format(hostname=hostname, name=spider_name)

    settings = {'STATSD_HOSTNAME': hostname, 'STATSD_PREFIX': prefix_pattern}
    crawler = CrawlerRunner(settings).create_crawler(Spider)
    spider = crawler._create_spider(spider_name)
    mw = StatsdMiddleware().from_crawler(crawler)

    mw.spider_opened(spider)
    mw.statsd_client = udp_client(expected_prefix)
    self.assertEqual(mw.statsd_prefix, expected_prefix)

    req = Request('http://scrapytest.org/')
    mw.process_request(req, spider)
    sock_check(mw.statsd_client._sock,
               1,
               'udp',
               val='{}.spider_reqs_issued:1|c'.format(expected_prefix))



