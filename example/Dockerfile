FROM ubuntu:16.04
MAINTAINER Zach Goldstein <zachgold@gmail.com>
VOLUME ["/opt/scrapy"]

RUN apt-get update && apt-get install -y \
    python\
    wget\
    gcc\
    python-dev\
    openssl\
    libssl-dev\
    libxml2-dev\
    libxslt-dev\
    libffi-dev
RUN cd /tmp; wget https://bootstrap.pypa.io/get-pip.py; python get-pip.py
RUN mkdir -p /opt/scrapy
ADD ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
