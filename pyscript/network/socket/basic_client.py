#!/usr/bin/env python
#coding=utf-8
import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',8888))
client.send("Hi, Rocky!")
data = client.recv(2048)
print "Received data: {0}".format(data)
client.close()

