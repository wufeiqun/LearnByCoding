#!/usr/bin/env python3
import os
import socket
import argparse
import selectors


class TCPServer(object):
    """Simple TCPServer with selectors"""
    def __init__(self, host, port):
        self.pid = os.getpid()
        self.address = (host, port)
        self.sel = selectors.DefaultSelector()

    def accept(self, server_socket, mask):
        connection, client_address = server_socket.accept()
        print("收到{0}:{1}的连接!".format(*client_address))
        connection.setblocking(False)
        self.sel.register(connection, selectors.EVENT_READ, self.handle)

    def handle(self, connection, mask):
        data = connection.recv(1024)
        if data:
            print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"), *connection.getpeername()))
            connection.send("谢谢你!\n".encode())
        else:
            print("客户端: {0}:{1} 断开连接!".format(*connection.getpeername()))
            self.sel.unregister(connection)
            connection.close()

    def run(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen(100)
        self.sel.register(server, selectors.EVENT_READ, self.accept)
        print("Started server at {1}:{2}, PID: {0}".format(self.pid, *self.address))

        while True:
            events = self.sel.select(timeout=100)
            # key is a SelectorsKey instance including info about the client/server connection
            for key, mask in events:
                callback = key.data
                sock = key.fileobj
                callback(sock, mask)
        self.sel.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCP回显服务器!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()
    server = TCPServer(args.hostname, args.port)
    server.run()


