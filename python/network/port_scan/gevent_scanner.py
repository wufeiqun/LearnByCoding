#!/usr/bin/env python3
import sys
from datetime import datetime
import gevent
from gevent import Greenlet
import socket

def scanner_port(host, port):
    print("now scanner port : {}".format(port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((remoteServerIP, port))
    if result == 0:
        print("port {}: \t Open".format(port))

def init_thread(call_func, host):
    thread_list = []
    for i in range(1,65536):
        thread = Greenlet.spawn(call_func,host,i)
        thread_list.append(thread)
    return thread_list

def run_scanner(thread_list):
    gevent.joinall(thread_list)


remoteServer = input("pls enter remote host: \t")
remoteServerIP = socket.gethostbyname(remoteServer)

print("-" * 60)
print("pls warit , scanning remote host", remoteServerIP)
print("-" * 60)

threads=init_thread(scanner_port, remoteServerIP)
run_scanner(threads)


