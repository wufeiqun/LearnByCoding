#!/usr/bin/env python
#coding=utf-8
#在运行时知道一个函数有什么参数，通常是不可能的。另一个情况是一个函数能操作很多对象。更有甚者，调用自身的函数变成一种api提供给可用的应用。
#对于这些情况，python提供了两种特别的方法来定义函数的参数，允许函数接受过量的参数，不用显式声明参数。这些“额外”的参数下一步再解释。
#注意args和kwargs只是python的约定。任何函数参数，你可以自己喜欢的方式命名，但是最好和python标准的惯用法一致，以便你的代码，其他的程序员也能轻松读懂。

#位置参数
#在参数名之前使用一个星号，就是让函数接受任意多的位置参数。

def mutiply(*args):
	total = 1
	for arg in args:
		total+=arg
	return total

print mutiply(1,2,3,4)
#result is 11
#python把参数收集到一个元组中，作为变量args。显式声明的参数之外如果没有位置参数，这个参数就作为一个空元组。

#关键字参数
#python在参数名之前使用2个星号来支持任意多的关键字参数。
def accept(**kwargs):
	for keyword,value in kwargs.items():
		print '%s --> %s' %(keyword,value)

print accept(rocky='python',tony='c')
#result is: rocky --> python	tony --> c
#注意：kwargs是一个正常的python字典类型，包含参数名和值。如果没有更多的关键字参数，kwargs就是一个空字典。	
