#!/usr/bin/env python
#select是IO多路复用的一种技术, 优点是跨平台性好, 缺点是单个进程监控的fd数量有上限FD_SIZE, 一般是1024
import sys
import queue
import socket
import select


class TCPServer:
    def __init__(self, host, port, timeout):
        self.server_address = (host, port)
        self.server = self.create_server()
        self.inputs = [self.server]
        self.outputs = []
        self.timeout = timeout # 单位(秒)
        self.message_queues = {}

    def create_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind(self.server_address)
        server.listen(5)
        return server

    def handle_receive(self, readable):
        for sock in readable:
            if sock is self.server:
                connection, client_address = sock.accept()
                print("收到{0}:{1}的连接!".format(*client_address))
                connection.setblocking(False)
                self.inputs.append(connection)
                self.message_queues[connection] = queue.Queue()
            else:
                data = sock.recv(1024)
                if data:
                    print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"),
                        *sock.getpeername()))
                    self.message_queues[sock].put("谢谢你".encode())
                    if sock not in self.outputs:
                        self.outputs.append(sock)
                else:
                    print("客户端: {0}:{1} 断开连接!".format(*sock.getpeername()))
                    if sock in self.outputs:
                        self.outputs.remove(sock)
                    self.inputs.remove(sock)
                    sock.close()
                    del self.message_queues[sock]

    def handle_send(self, writable):
        for sock in writable:
            try:
                next_msg = self.message_queues[sock].get_nowait()
            except queue.Empty:
                self.outputs.remove(sock)
            else: # 当try语句执行的时候才执行else
                sock.send(next_msg)

    def handle_exception(self, exceptional):
        for sock in exceptional:
            print("Socket: {0}:{1} 发生异常!".format(*sock.getpeername()))
            self.inputs.remove(sock)
            if sock in self.outputs:
                self.outputs.remove(sock)
            sock.close()
            del self.message_queues[sock]

    def run(self):
        while self.inputs:
            try:
                readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, self.timeout)
                if not (readable or writable or exceptional):
                    print('在指定时间内未发现活跃的socket,这里可以做一些其它的事情, 然后继续监控!')
                    continue
                if readable:
                    self.handle_receive(readable)
                if writable:
                    self.handle_send(writable)
                if exceptional:
                    self.handle_exception(exceptional)
            except select.error:
                print("select error")



if __name__ == "__main__":
    server = TCPServer("0.0.0.0", 8888, 10)
    server.run()
