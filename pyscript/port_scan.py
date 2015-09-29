#coding=utf-8
import socket
import sys

def usage():
	print '''
1.列出某个主机的所有开放端口
python port_scan.py ipaddr
2.查看某个主机的某个端口是否打开
python port_scan.py ipaddr port
'''

def scan(host,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.1)
    if s.connect_ex((host,int(port))) == 0:
        print port,'is open'

    s.close()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
        scan(host,port)
        sys.exit()
    elif len(sys.argv) == 1:
        host = '127.0.0.1'
    elif len(sys.argv) == 2:
        host = sys.argv[1]
    for port in xrange(1,65536):
        scan(host,port)
