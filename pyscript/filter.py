#!/usr/bin/env python
#coding=utf-8

print "\033[1;31;40m%s\033[0m" % "给一个列表,请找出其中的奇数\r\n"

num_list = [1,2,3,4,5,6,7,8,9]
print  "\033[1;31;40m%s\033[0m" % '方法一,迭代中过滤,效率低.'
print '--------------------------------------方法一-----------------------------------'
lista = []
for i in num_list:
	if i%2:
		lista.append(i)
print  'lista :',lista

print "\033[1;31;40m%s\033[0m" % '方法二,列表推导式.'
print '--------------------------------------方法二-------------------------------------'
listb = [i for i in num_list if i%2]
print 'listb :',listb

print "\033[1;31;40m%s\033[0m" % '方法三,使用内建函数filter.'
print '-------------------------------------方法三-------------------------------------'
def odd(x):
	return x%2

listc = filter(odd,num_list)
print 'listc :',listc


#1、filter(fn,list)是python的内建函数，它接受两个参数：一个函数和一个列表，返回的序列与第二个参数的类型一致； 2、而作为第一个参数传递给filter()的函数它本身应该是可接受一个参数的，函数若返回“True”，则此元素被包含在返回的序列中，。 3、第二个参数其实也可以是元组。

