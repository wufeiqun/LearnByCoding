#!/usr/bin/env python
#coding=utf-8
#simple muti hosts login program!
import sys
import os

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
	0: hostname	ipaddr	
	q: quit
'''
	user = 'test'
	servers = {
		'0': 'ipaddr'
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
