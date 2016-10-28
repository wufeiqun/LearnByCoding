#!/usr/bin/env python
#coding=utf-8
"""
多线程服务端的实现,每一个请求都会创建一个新的线程去处理
"""
import socket
import select
import threading

Thread_NUM = 0

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_addr = ("0.0.0.0", 8888)
server.bind(server_addr)
server.listen(5)
print "Started server at %s:%s..." % server_addr

def request(conn, addr):
    while 1:
        data = conn.recv(2048)
        if not data:
            break
        print "Received data: {0} from {1}".format(data, addr)
        conn.sendall(data)
        print "Echo data: {0}".format(data)
    conn.close()

while True:
    readable, writable, exceptional = select.select([server], [], [])
    if server in readable:
        newsocket, clientaddr = server.accept()
        Thread_NUM += 1
        t = threading.Thread(target=request, name="Server thread {0}".format(Thread_NUM), args=(newsocket, clientaddr,))
        t.start()
        print "Server thread {} has started...".format(Thread_NUM)
