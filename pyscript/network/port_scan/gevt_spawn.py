#!/usr/bin/env python
# coding:utf-8
from gevent import monkey
monkey.patch_all()
import gevent
import socket

def scan(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(0.5)
    if client.connect_ex(("118.193.81.214", port)) == 0:
        print "Port: {0} is open".format(port)
    client.close()

if __name__ == "__main__":
    greenlets = [gevent.spawn(scan, i) for i in xrange(1, 65535)]
    gevent.joinall(greenlets)
