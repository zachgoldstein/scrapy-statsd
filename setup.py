# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='scrapy-statsd-middleware',
    version='0.0.8',
    description='Statsd integration middleware for scrapy',
    long_description=readme,
    author='Zach Goldstein',
    author_email='zachgold@gmail.com',
    url='https://github.com/zachgoldstein/scrapy-statsd',
    license='Apache 2.0',
    packages=['scrapy_statsd_middleware'],
    install_requires=[
      'Scrapy>=1.0.5',
      'statsd==3.2.1'
    ],
    extras_require={
      'test': ['mock==2.0.0'],
    }
)
