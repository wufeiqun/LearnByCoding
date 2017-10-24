#!/usr/bin/env python
"""
简单的TCPServer
"""
import os
import argparse
import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"), *self.client_address))
            self.request.send("谢谢你!\n".encode())

    def finish(self):
        print("客户端: {0}:{1} 断开连接!".format(*self.client_address))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCP回显服务器!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()
    with socketserver.TCPServer((args.hostname, args.port), MyTCPHandler) as server:
        print("Started server at {0}:{1}, PID: {2}".format(args.hostname, args.port, os.getpid()))
        server.serve_forever()
