#!/usr/bin/env python3
import sys
import socket
from multiprocessing.dummy import Pool as ThreadPool

class Scanner:
    def __init__(self, host):
        self.host = host
        self.timeout = 0.5
        self.pool = ThreadPool(100)

    def scan(self, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(self.timeout)
        if client.connect_ex((self.host, port)) == 0:
            print("Port: {0} is open".format(port))

    def start(self):
        self.pool.map(self.scan, range(1, 10000))
        self.pool.close()
        self.pool.join()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        s = Scanner(sys.argv[1])
        s.start()
