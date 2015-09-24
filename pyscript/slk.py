#!/usr/bin/env python
#coding=utf-8
import sys
import os
import paramiko

def ssh_connect():
	print r'''
 _____   ____   _____ _  ____     __
|  __ \ / __ \ / ____| |/ /\ \   / /
| |__) | |  | | |    | ' /  \ \_/ /
|  _  /| |  | | |    |  <    \   /
| | \ \| |__| | |____| . \    | |
|_|  \_\\____/ \_____|_|\_\   |_|
'''
	print '''
Please select server:
	0: mmwd			128.199.197.146	
	1: sdzx			118.193.81.214
	2: aliyun		123.56.153.17
	q: quit
'''
	user = 'rocky'
	servers = {
		'0': '128.199.197.146',
		'1': '118.193.81.214',
		'2': '123.56.153.17'
	}

	input_num = raw_input(':')
	if input_num == 'q':
		sys.exit()
	elif not input_num in servers.keys():
		ssh_connect()
	else:
		os.system('ssh '+user+'@'+servers[input_num])

if __name__ == '__main__':
	ssh_connect()
