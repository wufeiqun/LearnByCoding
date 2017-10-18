#!/usr/bin/env python
#优点: 1. 相比较于poll, 不随着监控的fd数量的增长而变慢, 基于事件
import os
import queue
import select
import socket
import argparse


class TCPServer:
    def __init__(self, host, port, timeout):
        self.pid = os.getpid()
        self.server_address = (host, port)
        self.server = self.create_server()
        self.timeout = timeout  # 单位(秒)
        self.message_queues = {}
        self.READ_ONLY = (select.EPOLLIN | select.EPOLLPRI | select.EPOLLHUP | select.EPOLLERR)
        self.READ_WRITE = (self.READ_ONLY | select.EPOLLOUT)
        self.epoller = select.epoll()
        self.epoller.register(self.server.fileno(), self.READ_ONLY)
        # 由于poll返回的是一个数组, 数组中的元素为元组, 元组格式为(fd, flag), 所以有必要定义一个fd_to_socket
        self.fd_to_socket = {self.server.fileno(): self.server}
        # 由于客户端socket关闭以后要删除fd_to_socket中保存的socket, 但是socket是value, 为了更加快速删除该条记录
        # 又定义了一个socket_to_fd字典
        self.socket_to_fd = {self.server: self.server.fileno()}

    def create_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind(self.server_address)
        server.listen(5)
        return server

    def handle_receive(self, sock):
        if sock is self.server:  # 说明是有新的客户端请求进来
            connection, client_address = sock.accept()
            print("收到{0}:{1}的连接!".format(*client_address))
            connection.setblocking(False)
            self.fd_to_socket[connection.fileno()] = connection
            self.socket_to_fd[connection] = connection.fileno()
            # 将新来的客户端socket注册到监听列表中
            self.epoller.register(connection.fileno(), self.READ_ONLY)
            # 这里使用了队列, 保存要返回的数据, 如果只是学习poll使用的话可以去掉, 让每个socket返回相同数据即可
            self.message_queues[connection] = queue.Queue()
        else:  # 说明已经建立连接的socket有数传送过来据等待接收
            data = sock.recv(1024) # 这里不能使用while阻塞地获取完数据, 因为是非阻塞式的socket, 通过poll的不停遍历实现数据的全部获取
            if data:
                print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"),
                                                         *sock.getpeername()))
                self.message_queues[sock].put("谢谢你\n".encode())
                # 修改该socket监控状态为读写
                self.epoller.modify(sock, self.READ_WRITE)
            else:  # 客户端断开连接
                print("客户端: {0}:{1} 断开连接!".format(*sock.getpeername()))
                # 取消该socket的注册信息
                self.epoller.unregister(sock)
                # 删除该socket的消息队列
                del self.message_queues[sock]
                # 从fd字段中删除该socket
                del self.fd_to_socket[self.socket_to_fd[sock]]
                del self.socket_to_fd[sock]
                # 关闭该socket
                sock.close()

    def handle_send(self, sock):
        try:
            next_msg = self.message_queues[sock].get_nowait()  # 从消息队列里获取数据(前面填充到该队列里的数据)
        except queue.Empty:  # 该socket的消息队列为空的时候表示已经读取并回复了, 这时候应该只监听该socket是否可读即可
            self.epoller.modify(sock, self.READ_ONLY)
        else:
            sock.send(next_msg)

    def handle_exception(self, sock):
        print("连接: {0}:{1} 发生异常!".format(*sock.getpeername()))
        # 取消该socket的注册信息
        self.epoller.unregister(sock)
        # 删除该socket的消息队列
        del self.message_queues[sock]
        # 从fd字段中删除该socket
        del self.fd_to_socket[self.socket_to_fd[sock]]
        del self.socket_to_fd[sock]
        sock.close()

    def run(self):
        print("Started server at {0}:{1}, PID: {2}".format(*self.server_address, self.pid))
        while True:
            events = self.epoller.poll(self.timeout)
            if not events:
                print("继续事件监听中...")
                continue
            for fd, event in events:
                sock = self.fd_to_socket[fd]
                if event == select.EPOLLIN:
                    self.handle_receive(sock)
                elif event == select.EPOLLOUT:  # 说明该socket是可写状态, 一般只要没有在可读状态的时候一个socket都是出于可写状态的
                    self.handle_send(sock)
                elif event in (select.EPOLLERR, select.EPOLLHUP):
                    self.handle_exception(sock)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCPServer!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    parser.add_argument("--timeout", dest="timeout", type=int, default=5, metavar="超时时间(秒)", help="请输入超时时间")
    args = parser.parse_args()
    server = TCPServer(args.hostname, args.port, args.timeout)
    server.run()
