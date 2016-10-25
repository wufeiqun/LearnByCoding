#!/usr/bin/env python
# coding:utf-8
import gevent
from gevent import monkey
monkey.patch_socket()
import time
import socket
import traceback
import threading
import multiprocessing
import requests
from bs4 import BeautifulSoup


class Site(object):
    """
        To test the advantage of the gevent compared to multithreading,
    multiprocessing,I crawled the http://www.alexa.com/topsites/global
    and resovle the domain names contains in the page.
    """
    def __init__(self):
        # "http://www.alexa.com/topsites/global;[0-19]"
        self.baseURL = "http://www.alexa.com/topsites/global;"
        self.timeout = 5  # seconds
        self.totalPage = 20  # 0-19
        self.domain = []
        self.ipaddr = []

    def getURList(self, page):
        """Get all the domains of the page"""
        urList = []
        req = requests.get(self.baseURL+str(page))
        soup = BeautifulSoup(req.text, "lxml")
        lst = soup.find_all(class_="site-listing")
        for l in lst:
            self.domain.append(l.find("a").string)

    def resolve(self, domain):
        """
        socket.getaddrinfo(host, port[, family[, socktype[, proto[, flags]]]])
        Just return the Ipv4 TCP info.
        """
        try:
            ret = socket.getaddrinfo(domain, 80, 2, 1, 6)
            ip = ret[0][4][0]
            self.ipaddr.append(ip)
        except Exception, e:
            print traceback.format_exc(e)

    def common(self):
        """
        usual method with for ... in xrange.
        """
        start = time.time()
        for page in xrange(self.totalPage):
            self.getURList(page)
        end = time.time()
        print "***" * 10 + "common" + "***" * 10
        print "Total domains: {0}".format(len(self.domain))
        print "Total used %0.2f seconds." % (end - start)

    def multithread(self):
        """
        Using multithread.
        """
        self.domain = []  # clear it before run
        start = time.time()
        threads = []
        for page in xrange(self.totalPage):
            t = threading.Thread(target=self.getURList, args=(page,))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        end = time.time()
        print "***" * 10 + "multithreading" + "***" * 10
        print "Total domains: {0}".format(len(self.domain))
        print "Total used %0.2f seconds." % (end - start)

    def multiprocess(self):
        """
        Using multiprocess.
        """
        self.domain = multiprocessing.Manager().list()
        start = time.time()
        processes = []
        for page in xrange(self.totalPage):
            p = multiprocessing.Process(target=self.getURList, args=(page,))
            p.start()
            processes.append(p)
        for process in processes:
            process.join()
        end = time.time()
        print "***" * 10 + "multiprocessing" + "***" * 10
        print "Total domains: {0}".format(len(self.domain))
        print "Total used %0.2f seconds." % (end - start)

    def gevt(self):
        """
        Using gevent.
        """
        self.domain = []
        start = time.time()
        greenlets = []
        for page in xrange(self.totalPage):
            greenlets.append(gevent.spawn(self.getURList, page))
        gevent.joinall(greenlets)
        end = time.time()
        print "***" * 10 + "gevent" + "***" * 10
        print "Total domains: {0}".format(len(self.domain))
        print "Total used %0.2f seconds." % (end - start)


if __name__ == "__main__":
    site = Site()
    site.common()
    site.multithread()
    # site.multiprocess()
    site.gevt()
