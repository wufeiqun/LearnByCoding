# !/usr/bin/env python
"""
简单的TCP回显服务
"""
import os
import socket
import argparse


class  EchoServer:
    def __init__(self, host, port):
        self.pid = os.getpid()
        self.address = (host, port)

    def run(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen(5)
        print("Started server at {0}:{1}, PID: {2}".format(*self.address, self.pid))
        while True:
            connection, client_address = server.accept()
            print("收到{0}:{1}的连接!".format(*client_address))
            self.handler(connection, client_address)

    def handler(self, connection, client_address):
        while True:
            data = connection.recv(2048)
            if not data:
                break
            print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"), *client_address))
            connection.send("谢谢你!\n".encode())
        print("客户端: {0}:{1} 断开连接!".format(*client_address))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCP回显服务器!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()
    e = EchoServer(args.hostname, args.port)
    e.run()
