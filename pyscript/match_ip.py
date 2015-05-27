#!/usr/bin/env python
#coding=utf-8
#matching ip address from nginx logs.

import re 

#text 是nginx的3条访问记录.
text = '''108.162.215.174 - - [23/Mar/2015:00:08:00 +0800] "GET / HTTP/1.1" 301 5 "-" 
108.162.215.174 - - [23/Mar/2015:00:08:03 +0800] "GET /forum.php HTTP/1.1" 200 484-" 
108.162.215.174 - - [23/Mar/2015:00:08:39 +0800] "GET / HTTP/1.1" 301 5 "-" "Mozilla/5.0"
'''
pat = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

print '目标文本为:',text
print '-------------------------------------我是可爱的分割线--------------------------------------------------------\n'

print '匹配的IP地址为:', re.findall(pat,text)
