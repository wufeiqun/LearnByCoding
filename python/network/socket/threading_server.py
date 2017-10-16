#!/usr/bin/env python
"""
多线程版本的回显服务,每一个请求都会创建一个新的线程去处理
"""
import socket
import argparse
import threading


class EchoServer:
    def __init__(self, host, port):
        self.thread_num = 0
        self.address = (host, port)

    def handler(self, conn, addr):
        while True:
            data = conn.recv(2048)
            if not data:
                break
            print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"), *addr))
            conn.sendall("谢谢你!\n".encode())
        print("Closed from {0}:{1}".format(*addr))

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen(5)

        print("Started server at {0}:{1}...".format(*self.address))

        while True:
            newsocket, clientaddr = server.accept()
            self.thread_num += 1
            thread = threading.Thread(target=self.handler, args=(newsocket, clientaddr,))
            thread.start()
            print("Server thread {0} has started to process {1}:{2}".format(self.thread_num, *clientaddr))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCP回显服务器!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()
    server = EchoServer(args.hostname, args.port)
    server.run()
