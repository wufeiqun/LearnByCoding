#!/usr/bin/env python
# coding:utf-8
import socket
from multiprocessing import Pool

def scan(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(0.5)
    if client.connect_ex(("118.193.81.214", port)) == 0:
        print "Port: {0} is open".format(port)
    client.close()

if __name__ == "__main__":
    pool = Pool(10)
    pool.map(scan, xrange(1, 65535))
    pool.close()
    pool.join()
