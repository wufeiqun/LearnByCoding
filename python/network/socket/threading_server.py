#!/usr/bin/env python
"""
多线程版本的回显服务,每一个请求都会创建一个新的线程去处理
"""
import socket
import threading


class EchoServer:
    def __init__(self, host, port):
        self.thread_num = 0
        self.address = (host, port)

    def request(self, conn, addr):
        while 1:
            data = conn.recv(2048)
            if not data:
                break
            print("Received data: {0} from {1}:{2}".format(data, *addr))
            conn.sendall(data)
        print("Closed from {0}:{1}".format(*addr))

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen(5)

        print("Started server at {0}:{1}...".format(*self.address))

        while True:
            newsocket, clientaddr = server.accept()
            self.thread_num += 1
            t = threading.Thread(target=self.request, args=(newsocket, clientaddr,))
            t.start()
            print("Server thread {0} has started...".format(self.thread_num))


if __name__ == "__main__":
    s = EchoServer("0.0.0.0", 8888)
    s.start()
