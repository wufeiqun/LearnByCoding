#!/usr/bin/env python
#coding=utf-8
"""
这是单线程阻塞版本的server,第一个连接能够处理,第二个链接只能排队,等待第一个连接关闭以后服务端才能够处理第二个的请求.
"""
import socket

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
    newsocket, clientaddr = server.accept()
    request(newsocket, clientaddr)
