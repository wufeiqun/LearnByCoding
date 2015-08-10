#!/usr/bin/env python
#coding=utf-8
#/home/qfpay/scripts/supervisor_record.txt维护着本机所有supervisor的记录,这样可以实现自动化上线并且加上监控.此脚本逐一读取里面的记录并查看状态~
#用法: 默认返回0或者2.(0代表OK,2代表有问题.)
#加上参数`show`来显示所有程序的状态
#

import os
import sys

def get_status():
	try:
		supervisor_record = open('/home/qfpay/script/supervisor_record.txt','r').readlines()
	except:
		print 'supervisor_record.txt not found,please check it.'
		sys.exit(1)

	sicked_program = []
	for check_status in supervisor_record:
		for stat in os.popen(check_status).readlines():
			if not 'RUNNING' in stat:
				sicked_program.append(stat.split()[0])
			else:
				pass

	if sicked_program == []:
		print 'All services are OK'
		sys.exit(0)
	else:
		print str(sicked_program),' is not running,please check it.'
		sys.exit(2)


def show_status():
	try:
		supervisor_record = open('/home/qfpay/script/supervisor_record.txt','r').readlines()
	except:
		print 'supervisor_record.txt not found,please check it.'
		sys.exit(1)

	for check_status in supervisor_record:
		for stat in os.popen(check_status).readlines():
			#print stat.split()[0]+' is '+stat.split()[1]
			print stat.split()[0]+' is '+stat.split()[1]

if __name__ == '__main__':
	if len(sys.argv) == 1:
		get_status()
	else:
		show_status()
