# !/usr/bin/env python
"""
简单的TCP回显服务
"""
import os
import socket
import argparse


class  EchoServer:
    def __init__(self, host, port):
        self.pid = os.getpid()
        self.address = (host, port)

    def run(self):
        # 调用socket函数创建socket对象.本例是创建了一个TCP的连接.
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 设置地址复用,如果不设置的话,当调用socket.close()或者ctrl+c关闭服务器后还得经过TIME_WAIT的过程之后才能使用,马上启动的时候会提示端口被占用
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 将socket绑定到指定的地址上.socket.bind(address),address必须是一个双元素元组,(host,port),如果端口号正在被使用或者保留,
        # 或者主机名或ip地址错误，则引发socket.error异常
        server.bind(self.address)
        # 监听,准备好套接字,以便接受连接请求.括号里的参数为最大连接数,至少为1,超过则拒绝请求.
        server.listen(5)
        # 这里使用了一个while循环,如果不使用的话,经过一次连接后就会关闭.
        print("Started server at {0}:{1}, PID: {2}".format(*self.address, self.pid))  # Tuple unpacking
        while True:
            # 服务器套接字通过socket的accept方法等待客户连接请求,调用accept方法时，socket会进入'waiting'（或阻塞）状态。客户请求连接时，方法建立连接并返回服务器。accept方法返回一个含有俩个元素的元组，形如(connection,address)。第一个元素（connection）是新的socket对象，服务器通过它与客户通信；第二个元素（address）是客户的internet地址。
            newsocket, client_address = server.accept()
            print("收到{0}:{1}的连接!".format(*client_address))
            self.handler(newsocket, clientaddr)

    def handler(self, newsocket, clientaddr):
        #server端调用recv方法从客户端接收信息.调用recv 时，服务器必须指定一个整数，它对应于可通过本次方法调用来接收的最大数据量。recv方法在接收数据时会进入“blocked”状态，最后返回一个'字符串'，用它表示收到的数据。如果发送的数据量超过了recv所允许的，数据会被截短。多余的数据将缓冲于接收端。以后调用recv时，多余的数据会从缓冲区 删除(以及自上次调用recv以来，客户可能发送的其它任何数据)。
        while True:
            data = newsocket.recv(2048)
            if not data:
                break
            # 打印接收到的数据
            print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"), *clientaddr))
            newsocket.send("谢谢你!\n".encode())
        print("Connection closed from {0}:{1}".format(*clientaddr))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCP回显服务器!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()
    e = EchoServer(args.hostname, args.port)
    e.run()
