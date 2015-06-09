#!/usr/bin/env python
#coding=utf-8 
import socket 
import struct 
import fcntl 

def get_local_ip(ethname):
	#定义一个socket对象,这里定义的是UDP方式. 
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#返回的是1.1.1.1类似格式的IP地址.
	#socket.inet_ntoa 能把32位的ipv4二进制地址转换为1.1.1.1类似的格式.
	#s.fileno()返回socket的文件描述符,一个整数.
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24]) 

if __name__=='__main__': 
	print get_local_ip('eth0')
