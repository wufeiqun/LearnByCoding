#!/usr/bin/env python
#coding=utf-8
import socket
import time
import threading
import signal

server_addr = ('10.10.10.113',8888)
#server_addr = ('127.0.0.1',8888)
def multi_client(uid):
    locals()["client{0}".format(uid)] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    locals()["client{0}".format(uid)].connect(server_addr)
    while 1:
        locals()["client{0}".format(uid)].send("Hi, Rocky {0}!".format(uid))
        time.sleep(0.1)
    locals()["client{0}".format(uid)].close()

def single():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_addr)
    while 1:
        client.send("Hi, Qfpay~")
        time.sleep(1)
    client.close()


def main():
    threads = []
    for i in xrange(10):
        t = threading.Thread(target=multi_client, name="Client thread {0}".format(i), args=(i,))
        t.start()
        print "Client thread: {0} has started...".format(t.name)
        threads.append(t)
    for thread in threads:
        thread.join()

# register Ctrl+C signal
def handler(sig, frame):


if __name__ == "__main__":
    #single()
    main()
