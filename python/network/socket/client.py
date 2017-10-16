#!/usr/bin/env python
import sys
import time
import socket
import signal
import argparse
import threading


class Client:
    def __init__(self, host, port, thread_num):
        self.address = (host, port)
        self.thread_num = thread_num
        self.threads = []

    def client(self, tid):
        sock = "client{0}".format(tid)
        locals()[sock] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        locals()[sock].connect(self.address)
        locals()[sock].settimeout(10)

        while True:
            data = "你好, 服务器! 我是: {0}, 现在时间是: {1}".format(sock, time.strftime("%H:%M:%S", time.localtime()))
            locals()[sock].sendall(data.encode())
            print("发送: {0}".format(data))
            recv_data = locals()[sock].recv(1024)
            print("接收: {0}".format(recv_data.decode(encoding="utf-8", errors="ignore")))
            time.sleep(2)

    def run(self):
        for tid in range(self.thread_num):
            thread = threading.Thread(target=self.client, args=(tid,))
            thread.start()
            print("{0} has started...".format(thread.name))
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    # register Ctrl+C signal
    #def handler(sig, frame):


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCP客户端!")
    parser.add_argument("--hostname", dest="hostname", default="127.0.0.1", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    parser.add_argument("--thread", dest="thread", type=int, default=1, metavar="线程数", help="请输入要启动的客户端线程数")
    args = parser.parse_args()
    client = Client(args.hostname, args.port, args.thread)
    client.run()
