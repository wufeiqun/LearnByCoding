# !/usr/bin/env python
"""
基于selectors的简单的TCP回显服务
"""
import os
import socket
import selectors


class  EchoServer:
    def __init__(self, host, port):
        self.pid = os.getpid()
        self.address = (host, port)
        self.selector = selectors.DefaultSelector()

    def start(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen(100)
        server.setblocking(False)
        self.selector.register(server, selectors.EVENT_READ, self.accept)

        print("Started server at {0}:{1}, PID: {2}".format(*self.address, self.pid))

        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def accept(self, sock, mask):
        newsock, clientaddr = sock.accept()
        print("{0}:{1} connected!".format(*clientaddr))
        newsock.setblocking(False)
        self.selector.register(newsock, selectors.EVENT_READ, self.handler)

    def handler(self, newsock, mask):
        data = newsock.recv(2048)
        if data:
            print("Received data: {0} from {1}:{2}.".format(data, *newsock.getpeername()))
            print("This connection's fd is {0}".format(newsock.fileno()))
            newsock.send(data)
        else:
            print("Connection closed from {0}:{1}".format(*newsock.getpeername()))
            self.selector.unregister(newsock)
            newsock.close()


if __name__ == "__main__":
    e = EchoServer("0.0.0.0", 8888)
    e.start()
