#!/usr/bin/env python
# coding:utf-8
import gevent
from gevent import socket
from gevent.pool import Pool

from alexa import Site

site = Site()
site.gevt()
domains = site.domain

pool = Pool(10)
finished = 0

def job(url):
    global finished
    try:
        try:
            ip = socket.gethostbyname(url)
            print "{0}------>{1}".format(url, ip)
        except socket.gaierror as ex:
            print "{0} failed with {1}".format(url, ex)
    finally:
        finished += 1

with gevent.Timeout(2, False):
    for domain in domains:
        pool.spawn(job, domain)
    pool.join()

print "Finished within 2 seconds:{0}/{1}".format(finished, 500)
