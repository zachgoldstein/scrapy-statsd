======================================
Scrapy statsd middleware demonstration
======================================

Installation
============

pip install scrapy-statsd

.. code-block:: python

	DOWNLOADER_MIDDLEWARES = {
	  'statsd_middleware.StatsdMiddleware': 543,
	}
	
	SPIDER_MIDDLEWARES = {
	  'statsd_middleware.StatsdMiddleware': 543,
	}


Example Implementation
======================

see /example
install docker
run it via docker-compose
see the graphite graph...


Development
===========

cd ./scrapy_statsd_middleware 
nose2