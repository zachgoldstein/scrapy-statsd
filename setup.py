# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='scrapy-statsd-middleware',
    version='0.0.4',
    description='Statsd integration middleware for scrapy',
    long_description=readme,
    author='Zach Goldstein',
    author_email='zachgold@gmail.com',
    url='https://github.com/zachgoldstein/scrapy-statsd',
    license='Apache 2.0',
    packages=['scrapy_statsd_middleware'],
)
