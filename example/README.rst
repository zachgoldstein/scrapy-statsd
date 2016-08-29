======
Scrapy statsd middleware demonstration
======

This is a demonstration of scrapy-statsd, a middleware plugin for sending
scrapy stats to a local statsd daemon.

The basis of this project is dirbot, a Scrapy project to scrape websites from public web directories.

Docker Installation
=====

docker-compose build
docker-compose up -d
docker-compose -f ./example/docker-compose.yml run spider bash -c "cd ./opt/scrapy/dirbot/ && scrapy crawl dmoz"




Items
=====

The items scraped by this project are websites, and the item is defined in the
class::

    dirbot.items.Website

See the source code for more details.

Spiders
=======

This project contains one spider called ``dmoz`` that you can see by running::

    scrapy list

Spider: dmoz
------------

The ``dmoz`` spider scrapes the Open Directory Project (dmoz.org), and it's
based on the dmoz spider described in the `Scrapy tutorial`_

This spider doesn't crawl the entire dmoz.org site but only a few pages by
default (defined in the ``start_urls`` attribute). These pages are:

* http://www.dmoz.org/Computers/Programming/Languages/Python/Books/
* http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/

So, if you run the spider regularly (with ``scrapy crawl dmoz``) it will scrape
only those two pages.

.. _Scrapy tutorial: http://doc.scrapy.org/en/latest/intro/tutorial.html

Pipelines
=========

This project uses a pipeline to filter out websites containing certain
forbidden words in their description. This pipeline is defined in the class::

    dirbot.pipelines.FilterWordsPipeline
