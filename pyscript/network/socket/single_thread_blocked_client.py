#!/usr/bin/env python
#coding=utf-8
import socket
import time

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',8888))
while 1:
    client.send("Hi, Rocky!")
    data = client.recv(2048)
    print "Received data: {0}".format(data)
    time.sleep(1)
client.close()

