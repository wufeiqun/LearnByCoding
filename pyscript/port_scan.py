#!/usr/bin/bin python
# coding=utf-8
#Simple TCP port scanner.
import gevent
from gevent import monkey
monkey.patch_socket()
from gevent import socket
from gevent.pool import Pool
import time


def scan(port):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if client.connect_ex(("127.1",int(port))) == 0:
        print "{0} is open".format(port)
    client.close()

pool = Pool(500)

start = time.time()
pool.map(scan, xrange(1, 10000))
end = time.time()

print "Using %0.2f seconds." % (end - start)

start = time.time()
for port in xrange(1, 10000):
    scan(port)
end = time.time()
print "Using %0.2f seconds." % (end - start)
