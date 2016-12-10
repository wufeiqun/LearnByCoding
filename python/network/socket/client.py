#!/usr/bin/env python
# coding: utf-8
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

    def client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.address)

        while 1:
            data = b"Hi, Rocky!"
            client.sendall(data)
            print("Send data: {0} to {1}:{2}".format(data, *self.address))
            recv = client.recv(2048)
            print("Received data: {0} from {1}:{2}".format(recv, *self.address))
            time.sleep(1)

    def multi_client(self, tid):
        locals()["client{0}".format(tid)] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        locals()["client{0}".format(tid)].connect(self.address)

        while True:
            locals()["client{0}".format(tid)].send(b"Hi, Rocky " + bytes([tid]))
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
    if len(sys.argv) < 2:
        client.client()
    else:
        client.main()
