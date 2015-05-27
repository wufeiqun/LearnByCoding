#!/usr/bin/env python
#coding=utf-8
#mongodb version 3.0 。注意3.0跟之前的版本稍有不同。
#确保路径的存在。
import os
from datetime import datetime
from datetime import timedelta
from pwd import getpwnam

#define some basic info of mongodb.
today = datetime.now().strftime("%Y%m%d")
olddate = datetime.now() - timedelta(days=7)
bakdir = "/home/qfpay/backup/mongo"+today
deldir = "/home/qfpay/backup/mongo"+olddatei.strftime("%Y%m%d")
host = "127.0.0.1:27017"
database = ["test"] #想要备份的数据库列表。
user = "test"   #mongodb 的账号
passwd = "test" #mongodb的用户密码。

# 判断目录是否存在。如果不存在，创建并修改所属用户。

uid = getpwnam(sysuser).pw_uid

isexists = os.path.exists(bakdir)
if not isexists:
	os.makedirs(bakdir)
	print "成功创建备份目录 !!!"
#备份数据库。
for dbname in database:
	bakcmd = "mongodump --host %s --db %s --out %s" %(host,dbname,bakdir)
	if os.system(bakcmd) == 0:
		print dbname,"备份成功！！！"
	else:
		print dbname,"备份失败，请检查～"

#删除7天前的备份数据。
delcmd = "rm -rf %s" %(deldir)
delresult = os.system(delcmd)
if delresult == 0:
	print "成功删除7天前的备份文件！！！"
else:
	print "擦，删除7天前的备份文件失败，到底咋回事儿呀，是不是不存在呀？？？？？"
