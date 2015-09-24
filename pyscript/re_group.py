#!/usr/bin/env python
#coding=utf-8
import re

p = re.compile('\d-\d-\d')
m = p.match('2-3-1')
print m.group()
# 2-3-1
#如果不引入括号，增个表达式作为一个组，是group(0)

print m.group(1)
#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#IndexError: no such group
#如果引入括号，可以将上面的表达式分成3组，如下
p=re.compile('(\d)-(\d)-(\d)')
m=p.match('1-2-3')
print m.group()
#1-2-3
print m.group(0,2,1)
#('2-3-1', '2', '1')

#也可以给各个组取名字，例如，给第一个数组取名叫first
p=re.compile('(?P<first>\d)-(\d)-(\d)')
m=p.match('1-2-3')
print m.group(1)
# 1
print m.group('first')
# 1
