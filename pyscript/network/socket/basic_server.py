#!/usr/bin/env python
#coding=utf-8
#简单的socket TCP 回显服务器.
import socket

#调用socket函数创建socket对象.本例是创建了一个TCP的连接.
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#设置地址复用,如果不设置的话,当调用socket.close()或者ctrl+c关闭服务器后还得经过TIME_WAIT的过程之后才能使用,马上启动的时候会提示端口被占用
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#将socket绑定到指定的地址上.socket.bind(address),address必须是一个双元素元组,(host,port),如果端口号正在被使用或者保留，或者主机名或ip地址错误，则引发socke.error异常。
server_addr = ("0.0.0.0", 8888)
server.bind(server_addr)
#监听,准备好套接字,以便接受连接请求.括号里的参数为最大连接数,至少为1,超过则拒绝请求.
#这里使用了一个while循环,如果不使用的话,经过一次连接后就会关闭.
print "Started server at %s:%s..." % server_addr
while True:
	#服务器套接字通过socket的accept方法等待客户连接请求,调用accept方法时，socket会进入'waiting'（或阻塞）状态。客户请求连接时，方法建立连接并返回服务器。accept方法返回一个含有俩个元素的元组，形如(connection,address)。第一个元素（connection）是新的socket对象，服务器通过它与客户通信；第二个元素（address）是客户的internet地址。
    server.listen(1)
    newsocket, clientaddr = server.accept()
	#server端调用recv方法从客户端接收信息.调用recv 时，服务器必须指定一个整数，它对应于可通过本次方法调用来接收的最大数据量。recv方法在接收数据时会进入“blocked”状态，最后返回一个'字符串'，用它表示收到的数据。如果发送的数据量超过了recv所允许的，数据会被截短。多余的数据将缓冲于接收端。以后调用recv时，多余的数据会从缓冲区 删除(以及自上次调用recv以来，客户可能发送的其它任何数据)。
    data = newsocket.recv(2048)
    print "Received data: {0} from {1}.".format(data, clientaddr)
    #打印该套接字的文件描述符
    print "This connection's fd is {}".format(newsocket.fileno())
    #服务端调用send方法发送信息给客户端.
    newsocket.send(data)
    #newsocket.close()
