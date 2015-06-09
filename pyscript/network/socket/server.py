#!/usr/bin/env python
#coding=utf-8
#简单的socket小程序,服务端的实现.
import socket 

#调用socket函数创建socket对象.本例是创建了一个TCP的连接.
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#将socket绑定到指定的地址上.socket.bind(address),address必须是一个双元素元组,(host,port),如果端口号正在被使用或者保留，或者主机名或ip地址错误，则引发socke.error异常。
sock.bind(('0.0.0.0',8888))
#监听,准备好套接字,以便接受连接请求.括号里的参数为最大连接数,至少为1,超过则拒绝请求.
sock.listen(5)
#这里使用了一个while循环,如果不使用的话,经过一次连接后就会关闭.
while True:
	#服务器套接字通过socket的accept方法等待客户连接请求,调用accept方法时，socket会进入'waiting'（或阻塞）状态。客户请求连接时，方法建立连接并返回服务器。accept方法返回一个含有俩个元素的元组，形如(connection,address)。第一个元素（connection）是新的socket对象，服务器通过它与客户通信；第二个元素（address）是客户的internet地址。
    connection,address = sock.accept()
    try:
		#定义新通信对象的超时时间5s,若果客户端连接到server后5s内无操作则会报超时错误.
        connection.settimeout(5)
		#server端调用recv方法从客户端接收信息.调用recv 时，服务器必须指定一个整数，它对应于可通过本次方法调用来接收的最大数据量。recv方法在接收数据时会进入“blocked”状态，最后返回一个'字符串'，用它表示收到的数据。如果发送的数据量超过了recv所允许的，数据会被截短。多余的数据将缓冲于接收端。以后调用recv时，多余的数据会从缓冲区 删除(以及自上次调用recv以来，客户可能发送的其它任何数据)。
        buf = connection.recv(1024)    
    	#服务端调用send方法发送信息给客户端.
        connection.send('Welcome to Server!!')
			#打印客户端信息.
        print address,':',buf
    except socket.timeout:
        print 'Time out!!!'
	#关闭连接.
	connection.close()
