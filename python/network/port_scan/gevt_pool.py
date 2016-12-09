#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()
import socket
from gevent.pool import Pool

class Scanner:
    def __init__(self, host, timeout=0.5):
        self.host = host
        self.timeout = timeout

    def scan(port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(self.timeout)
        if client.connect_ex((self.host, port)) == 0:
            print("Port: {0} is open".format(port))
        client.close()

if __name__ == "__main__":
    pool = Pool(50)
    s = Scanner("121.42.185.92")
    pool.map(s.scan, range(1, 65536))
    pool.join()
