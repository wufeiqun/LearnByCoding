#!/usr/bin/env python
import sys
import time
import socket
import signal
import threading


class Client:
    def __init__(self, host, port):
        self.address = (host, port)
        self.thread_num = 10
        self.threads = []

    def multi_client(self, tid):
        client = locals()["client{0}".format(tid)]
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(self.address)
        client.settimeout(100)

        while True:
            locals()["client{0}".format(tid)].send(b"Hi, Rocky " + bytes([tid]))
            data = "你好, 服务器! 现在时间是: {0}".format(time.strftime("%H:%M:%S", time.localtime()))
            client.sendall(data.encode())
            print("发送: {0}".format(data))
            recv_data = client.recv(1024)
            print("接收: {0}".format(recv_data.decode(encoding="utf-8", errors="ignore")))
            time.sleep(2)
            time.sleep(0.1)

    def main(self):
        for tid in range(10):
            thread = threading.Thread(target=self.multi_client, args=(tid,))
            thread.start()
            print("{0} has started...".format(thread.name))
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

    # register Ctrl+C signal
    #def handler(sig, frame):


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888)
    #client = Client("150.95.155.56", 6666)
    if len(sys.argv) < 2:
        client.client()
    else:
        client.main()
