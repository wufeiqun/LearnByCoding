#!/usr/bin/env python
# coding:utf-8
import sys
import socket
import getopt

def scan(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(0.5)
    if client.connect_ex((host, int(port))) == 0:
        print "Port: {0} is open".format(port)
    client.close()

def usage():
    print """
usage: python basic.py [OPTION]...

A basic port scanner !

options:
  -i host/ip          ip address to be scanned.default: 127.0.0.1
  -t timeout          timeout in seconds, default: 0.5

General options:
  -h, --help             show this help message and exit
  --host host/ip         host/ip to be scanned.default: 127.0.0.1
  --timeout timeout      timeout in seconds, default: 0.5
  --version              show version information

Online help: <https://github.com/hellorocky/handyscript>

    """

def main(argv):
    try:
        options, args = getopt.getopt(argv, "hi:p:t", ["host=", "port=", "timeout=" ])
    except getopt.GetoptError as e:
        traceback.print_exc(e)
        usage()
        sys.exit(2)
    for opt, arg in options:
        if opt == "-h":
            usage()
        elif opt in ["-i", "--host"]:
            host = arg
        elif opt in ["-p", "--port"]:
            port = arg
        elif opt in ["-t", "--timeout"]:
            timeout = argv
    scan(host="127.0.0.1", port=80)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
    else:
        main(sys.argv[1:])
