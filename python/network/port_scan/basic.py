#!/usr/bin/env python3
import sys
import socket
import getopt

def main(host):
    def scanner(port):
class Scanner:
    def __init__(self, host):
        self.host = host

        self.timeout = 0.2
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(self.timeout)

    def scanner(self):
        for port in range(1, 65536):
            if self.client.connect_ex((self.host, int(port))) == 0:
                print("Port: {0} is open".format(port))
            client.close()






if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
