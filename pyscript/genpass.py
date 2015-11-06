#!/usr/bin/env python
#coding=utf-8
#随机生成指定长度的密码,没有包括符号,需要的话可以加上.
import sys
import string
import random

def genpass(length):
    strs = string.uppercase + string.lowercase + string.digits
    passwd = ''
    while len(passwd) < int(length):
        passwd = passwd + strs[random.choice(xrange(len(strs)))]
    print passwd
    print ''.join([random.choice(strs) for i in xrange(int(length))])

if __name__ == '__main__':
    if len(sys.argv) == 2:
        genpass(sys.argv[1])
    else:
        print '请输入指定长度的密码~'
