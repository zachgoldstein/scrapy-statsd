init:
	pip install -r requirements.txt

test:
	cd ./scrapy_statsd_middleware && nose2
