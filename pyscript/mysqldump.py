#!/usr/bin/env python
#coding=utf-8
#this pyscript it to backup the mysql databases to defined directory.
#version 1.0
#date 20150313
import os
import time
from datetime import datetime
from datetime import timedelta
import string

#define the backup directory.
back_dir = '/home/qfpay/BACKUP/'
if not os.path.exists(back_dir):
	os.mkdir(back_dir)
exist = os.path.exists(back_dir)
while exist:
	print 'successfully created dir',back_dir
        break
#define the mysql info.
databases = ['test1','test2']
ip_addr = '*.*.*.*'
port = '****'
user = '****'
passwd = ['******']

#start backup databases!
today = datetime.now()
for dbname in databases:
    today_sql = back_dir + dbname + '_' +today.strftime('%Y%m%d')+'.sql'
    sql_cmd = "mysqldump -h %s -u%s -p'%s' %s > %s" %(ip_addr,user,passwd[0],dbname,today_sql)
    if os.system(sql_cmd) == 0:
	    print dbname,'backup successfully !!'
    else:
	    print dbname,'backup faild !!!'

#delete 2 days ago bakfiles.
for dbname in databases:
    days = timedelta(days=2)
    del_day =  today - days
    del_sql = dbname +'_'+ del_day.strftime('%Y%m%d') +'.sql'
    try:
        os.remove(back_dir + del_sql)
        print 'Successfully delete 2 days before data!'
    except:
        print "Maybe the " + del_sql +  " didn't exist......"
#change the dir mode.

os.system('chown -R qfpay.qfpay /home/qfpay/BACKUP')
