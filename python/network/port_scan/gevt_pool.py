#!/usr/bin/env python
# coding:utf-8
from gevent import monkey
monkey.patch_all()
import socket
from gevent.pool import Pool

def scan(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(0.5)
    if client.connect_ex(("118.193.81.214", port)) == 0:
        print "Port: {0} is open".format(port)
    client.close()

if __name__ == "__main__":
    pool = Pool(500)
    pool.map(scan, xrange(1, 65536))
    pool.join()
