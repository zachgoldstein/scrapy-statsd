======================================
Scrapy statsd middleware demonstration
======================================

Usage
=====

pip install scrapy-statsd-middleware

.. code-block:: python

	DOWNLOADER_MIDDLEWARES = {
	  'statsd_middleware.StatsdMiddleware': 543,
	}
	
	SPIDER_MIDDLEWARES = {
	  'statsd_middleware.StatsdMiddleware': 543,
	}

There's also a few settings that you can use:

* STATSD_HOSTNAME - Defaults to the current machine's hostname
* STATSD_PREFIX - Defaults to "hostname.spider-name."
* STATSD_HOST_IP - Defaults to "0.0.0.0"

This will increment statsd with the following:
* requests (spider_reqs_issued)
* response (spider_resps_received)
* errors (error_KeyError, where KeyError is whatever the error name is)
* items processed (processed_Product, where Product is whatever the item class name is)

Example Implementation
======================

An example implementation of this middleware is in /example
It includes a docker-compose file that describes how to use this middleware with statsd & graphite


Example Installation & Usage
============================

* Build the docker images `docker-compose build`
* Start the statsd container `docker-compose up -d`
* Run the example spider: `docker-compose -f ./example/docker-compose.yml run spider bash -c "cd ./opt/scrapy/dirbot/ && scrapy crawl dmoz"`

You can see a live graphite dashboard at http://0.0.0.0/dashboard
You should see stats show up under something like "stats.Z-MacBook-Pro.local.dmoz.spider_reqs_issued"

Development
===========

You can run the tests via `make test` 
