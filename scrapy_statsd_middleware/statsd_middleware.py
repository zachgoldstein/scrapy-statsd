import socket

from scrapy import signals
from statsd import StatsClient


class StatsdMiddleware(object):
  """
  Send statistics to local statsd daemon.

  This is run as both downloader and spider middleware (to record all exceptions)
  Statistics with be recorded for each req, resp and exception.
  """

  def __init__(self):
    self.statsd_client = None

  def process_request(self, request, spider):
    self.statsd_client.incr("spider_reqs_issued")

  def process_response(self, request, response, spider):
    self.statsd_client.incr("spider_resps_received")
    return response

  def process_exception(self, request, exception, spider):
    self.statsd_client.incr("error_{}".format(type(exception).__name__))

  def process_spider_output(self, response, result, spider):
    for spider_result in result:
      self.statsd_client.incr("processed_{}".format(type(spider_result).__name__))

    return result

  def process_spider_exception(self, response, exception, spider):
    self.statsd_client.incr("error_{}".format(type(exception).__name__))

  @classmethod
  def from_crawler(cls, crawler):
    o = cls()
    crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
    return o

  def spider_opened(self, spider):
    try:
      hostname = spider.settings["STATSD_HOSTNAME"]
      if hostname is None:
        raise ValueError
    except (KeyError, ValueError):
      hostname = socket.gethostname()

    try:
      name = spider.name
    except AttributeError:
      name = "spider"

    try:
      prefix = spider.settings["STATSD_PREFIX"]
      if prefix is None:
        raise ValueError
      self.statsd_prefix = prefix.format(hostname=hostname, name=name)
    except (AttributeError, ValueError):
      self.statsd_prefix = "{}.{}.".format(hostname, name)

    try:
      host_ip = spider.settings["STATSD_HOST_IP"]
      if host_ip is None:
        raise ValueError
    except (KeyError, ValueError):
      host_ip = "0.0.0.0"

    self.statsd_client = StatsClient(host=host_ip,
                                     port=8125,
                                     prefix=self.statsd_prefix,
                                     maxudpsize=512,
                                     ipv6=False)
    spider.logger.info("Initialised statsd client with name {} "
                       "on host {}".format(self.statsd_prefix,host_ip))

