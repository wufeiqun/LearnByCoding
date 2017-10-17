#!/usr/bin/env python
"""
多线程版本的TCPServer
"""
import socket
import argparse
import threading


class EchoServer:
    def __init__(self, host, port):
        self.thread_num = 0
        self.address = (host, port)
        self.pid = os.getpid()

    def handler(self, connection, client_address):
        while True:
            data = connection.recv(2048)
            if not data:
                break
            print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"), *client_address))
            connection.sendall("谢谢你!\n".encode())
            print("客户端: {0}:{1} 断开连接!".format(*client_address))

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen(5)

        print("Started server at {0}:{1}, PID: {2}".format(*self.address, self.pid))

        while True:
            connection, client_address = server.accept()
            self.thread_num += 1
            thread = threading.Thread(target=self.handler, args=(connection, client_address,))
            thread.start()
            print("Server thread {0} has started to process {1}:{2}".format(self.thread_num, *client_address))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCPServer!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()
    server = EchoServer(args.hostname, args.port)
    server.run()
