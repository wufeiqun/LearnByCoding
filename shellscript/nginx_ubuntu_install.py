#!/usr/bin/env python
#coding=utf-8
#ubuntu version:14.04
#nginx version:1.8.0
#installed folder:/home/rocky/nginx
#date 2015-05-25
#owner:rocky
import os

user = 'rocky'
homedir = '/home/'+user
#判断用户rocky是否存在,不存在就创建.
with open('/etc/passwd') as f:
	if user in f.read():
		print 'User is exists,please go on !!!'
	else:
		os.system('mkdir '+homedir)
		os.system('useradd -d '+homedir+' '+user)
		os.system('chown -R '+user+':'+user+' '+homedir)
		print 'User %s created successfully!!!' %(user)

#安装一些依赖包.
print '------------------------------安装一些依赖包.---------------------------------'
aptcmd = 'sudo apt-get install libpcre3-dev libssl-dev openssl -y'
try:
	os.system(aptcmd)
except:
	print 'something wrong with apt-get install....please check it.'

