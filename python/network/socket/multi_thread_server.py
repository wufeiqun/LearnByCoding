#!/usr/bin/env python
#coding=utf-8
"""
多线程服务端的实现,每一个请求都会创建一个新的线程去处理
"""
import socket
import select
import threading


class Server:
    def __init__(self):
        self.thread_num = 0
        self.server_addr = ("127.0.0.1", 8888)
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.server_addr)
        self.server.listen(5)
        print "Started server at {0}:{1}...".format(*self.server_addr)

    def request(self, conn, addr):
        while 1:
            data = conn.recv(2048)
            if not data:
                break
            print "Received data: {0} from {1}".format(data, addr)
            conn.sendall(data)
            print "Echo data: {0}".format(data)
        conn.close()

    def start(self):
        while True:
            newsocket, clientaddr = self.server.accept()
            self.thread_num += 1
            t = threading.Thread(target=self.request, name="Server thread {0}".format(self.thread_num), args=(newsocket, clientaddr,))
            t.start()
            print "Server thread {} has started...".format(self.thread_num)

if __name__ == "__main__":
    s = Server()
    s.start()
