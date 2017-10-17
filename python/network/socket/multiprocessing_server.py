#!/usr/bin/env python
"""
多进程版本的TCPServer
"""
import os
import socket
import argparse
import traceback
import multiprocessing


class EchoServer:
    def __init__(self, host, port):
        self.process_num = 0
        self.address = (host, port)
        self.pid = os.getpid()

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

        print("Started server at {0}:{1} with pid: {2}...".format(*self.address, self.pid))

        while True:
            connection, client_address = server.accept()
            self.process_num += 1
            process = multiprocessing.Process(target=self.handler, args=(connection, client_address,))
            process.daemon = True
            process.start()
            print("Server process {0} has started to process {1}:{2}".format(self.process_num, *client_address))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCPServer!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()
    server = EchoServer(args.hostname, args.port)
    try:
        server.run()
    except:
        traceback.print_exc()
    finally:
        for process in multiprocessing.active_children():
            print("关闭子进程: {0}".format(process.name))
            process.terminate()
            process.join()
