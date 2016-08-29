from __future__ import with_statement

import socket

import mock
from nose.tools import eq_
from statsd import StatsClient
from statsd import TCPStatsClient

ADDR = (socket.gethostbyname('localhost'), 8125)


# proto specific methods to get the socket method to send data
send_method = {
  'udp': lambda x: x.sendto,
  'tcp': lambda x: x.sendall,
}


# proto specific methods to create the expected value
make_val = {
  'udp': lambda x, addr: mock.call(str.encode(x), addr),
  'tcp': lambda x, addr: mock.call(str.encode(x + '\n')),
}


def udp_client(prefix=None, addr=None, port=None, ipv6=False):
  if not addr:
    addr = ADDR[0]
  if not port:
    port = ADDR[1]
  sc = StatsClient(host=addr, port=port, prefix=prefix, ipv6=ipv6)
  sc._sock = mock.Mock()
  return sc


def tcp_client(prefix=None, addr=None, port=None, timeout=None, ipv6=False):
  if not addr:
    addr = ADDR[0]
  if not port:
    port = ADDR[1]
  sc = TCPStatsClient(host=addr, port=port, prefix=prefix, timeout=timeout,
                      ipv6=ipv6)
  sc._sock = mock.Mock()
  return sc


def sock_check(sock, count, proto, val=None, addr=None):
  send = send_method[proto](sock)
  eq_(send.call_count, count)
  if not addr:
    addr = ADDR
  if val is not None:
    eq_(
      send.call_args,
      make_val[proto](val, addr),
    )