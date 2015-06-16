#!/usr/bin/env python
#coding=utf-8

def createip(addr):
    iplist = []
    parts = addr.split('/')
    baseip = ip2bin(parts[0])
    subnet = int(parts[1])
    ipprefix = baseip[:subnet]
    for i in range(2**(32-subnet)):
        iplist.append(bin2ip(ipprefix+dec2bin(i,(32-subnet))))
    print iplist[:5]


def dec2bin(num,d=None):
    s = ''
    while num > 0:
        if num&1:
            s = '1' + s
        else:
            s = '0' + s
        num >>= 1
    if d is not None:
        while len(s) < d:
            s = '0' + s
    if s == '': s = '0'
    return s

def ip2bin(ip):
    ipbin = ''
    ipparts = ip.split('.')
    for i in ipparts:
        ipbin += dec2bin(int(i),8)
    return ipbin

def bin2ip(b):
    ipaddr = ''
    for ippart in range(0,len(b),8):
        ipaddr += str(int(b[ippart:ippart+8],2))+'.'
    return ipaddr[:-1]

if __name__ == '__main__':
    createip('192.168.2.1/24')
