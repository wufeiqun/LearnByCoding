#coding=utf-8
import socket
import sys

def scan(port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.1)
    if s.connect_ex((sys.argv[1],port)) == 0:
        print port

    s.close()

if __name__ == '__main__':
   map(scan,xrange(10000))
