#coding=utf-8
#randomlly return the unused port with the specified range.
import socket
import sys
import random

def port_select(port_start=4000,port_end=10000):
	ports = []
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(0.5)
	for port in range(port_start,port_end):
		if s.connect_ex(('127.0.0.1',port)) != 0:
			ports.append(port)
	s.close()
	recommand_port = random.choice(ports)	
	print recommand_port

if __name__ == '__main__':
	port_select()	
