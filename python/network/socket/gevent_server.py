#!/usr/bin/env python
"""
简单的TCPServer
"""
import os
import socket
import argparse

from gevent.server import StreamServer


class TCPServer:
    def __init__(self, host, port):
        self.pid = os.getpid()
        self.address = (host, port)

    def handler(self, connection, client_address):
        while True:
            data = connection.recv(2048)
            if not data:
                break
            print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"), *client_address))
            connection.send("谢谢你!\n".encode())
        print("客户端: {0}:{1} 断开连接!".format(*client_address))

    def run(self):
        print("Started server at {0}:{1}, PID: {2}".format(*self.address, self.pid))
        server = StreamServer(self.address, self.handler)
        server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCP回显服务器!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()
    server = TCPServer(args.hostname, args.port)
    server.run()
