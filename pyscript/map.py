#!/usr/bin/env python
#coding=utf-8
#python map函数举例。
#map接收一个函数和一个可迭代对象（如列表）作为参数，用函数处理每个元素，然后返回新的列表。
#
lista = [1,2,3,4,5,6]
result1 = map(lambda x:x*5,lista)
print result1
#result1 = [5, 10, 15, 20, 25, 30]

#对这个列表进行迭代求平方，并返回一个列表的结果。可以定义一个函数，也可以使用map函数。如下面。
def sqrt():
	listb = []
	for it in lista:
		item = it**2
		listb.append(item)
	print listb
#listb = [1, 4, 9, 16, 25, 36] 
sqrt()
#使用map函数计算。
result2 = map(lambda x:x**2,lista)
print result2
#result2 跟上面函数中的结果一样的。

#或者把函数部分拿出来。
def qr(x):
	return x**2

result3 = map(qr,lista)
print result3
