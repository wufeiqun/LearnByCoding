#!/usr/bin/env python
#coding=utf-8

#方法一,利用python自带的函数bin()可以返回二进制(str).
#方法二,定义一个函数来实现.python不能直接操作二进制数字,但是有相关的运算符&按位与运算.遍历所输入十进制数字的二进制字符,利用&判断为0 or 1,并新建一个字符串来存放得到的二进制.最后返回.
def ip2bin(ip):
	s = ''
	num_list = ip.split('.')
	for n in num_list:
		s += dec2bin(int(n),8)
	return s

def dec2bin(num,length=None):
	s = '' #定义一个空的字符串来存放结果.
	while num > 0:
		if num&1: #判断二进制的最后一位0 or 1.
			s = '1' + s
		else:
			s = '0' + s
		num >>= 1 # 把一个数的比特向右移一定数目
	if length != None:
		while len(s) < length:
			s = '0' + s
	if s == '':
		s = '0'
	return s

if __name__ == '__main__':
	print ip2bin('192.168.1.1')
		
