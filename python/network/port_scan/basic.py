#!/usr/bin/env python3
import sys
import socket
import getopt

def main(host):
    def scanner(port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.2)
        if client.connect_ex((host, int(port))) == 0:
            print("Port: {0} is open".format(port))
        client.close()
    for port in range(1, 65536):
        scanner(port)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
