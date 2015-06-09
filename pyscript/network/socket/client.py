#!/usr/bin/env python
#coding=utf-8
#在终端运行server.py，然后运行clien.py，会在终端打印“welcome to server!"。如果更改client.py的sock.send('1')为其它值在终端会打印”please go out!“，更改time.sleep(2)为大于5的数值， 服务器将会超时。
import socket
import time
import sys
#创建socket对象,必须跟服务器的一样,不一样会被拒绝.
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#调用socket对象的connect方法去连接服务端.
sock.connect(('127.0.0.1',8888))
#使用time模块的sleep方法,测试服务端的timeout功能.
time.sleep(4)
#调用send方法发送信息给服务端.
sock.send(sys.argv[1])
#调用recv方法接收服务端发来的信息.
print sock.recv(1024)
#关闭连接.
sock.close()

