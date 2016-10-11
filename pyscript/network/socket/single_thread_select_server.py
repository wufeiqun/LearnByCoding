#!/usr/bin/env python
#coding=utf-8
import socket
import select

"""
单线程,select IO模型,select遍历注册到它上面的socket 文件描述符的过程是阻塞的,如果不加上timeout参数,它就会一直阻塞直到有活跃的socket fd出现.
运行这个服务后,有服务进来,服务端就会处理,但是再打开一个新的客户端后,就会阻塞住,直到第一个请求结束,服务端才能处理第二个请求.
"""

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
        print "Received data: {0} from {1}.".format(data, addr)
        conn.send(data)
        print "Responsed data: {0}".format(data)
    conn.close()

while True:
    readable, writable, exceptional = select.select([server], [], [])
    print "select find active fd ..."
    if server in readable:
        newsocket, clientaddr = server.accept()
        request(newsocket, clientaddr)
