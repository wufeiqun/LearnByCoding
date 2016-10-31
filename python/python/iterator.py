#!/usr/bin/env python
# coding:utf-8
"""
List/tuple 等collections是可迭代的也就是说是iterable,但它们不是iterator.
iterable 只实现了__iter__方法.
iterator 同时实现了__iter__和next方法,__iter__返回本身,next返回下一个元素

可以直接作用于for循环的对象统称为可迭代对象,也就是iterable可以用for循环
要把list,str,tuble等iterable变成iterator的时候可以使用iter函数.
"""
from collections import Iterable,Iterator

#True,list is iterable
print isinstance([], Iterable)

#False,list is not iterator
print isinstance([], Iterator)

#使用iter方法可以把iterable变成iterator
print isinstance(iter("ABC"), Iterator)


class MyIterator(object):
    def __init__(self, lst):
        self.lst   = lst
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index == len(self.lst):
            raise STOPIteration
        self.index += 1
        return self.lst[self.index-1]

if __name__ == "__main__":
    i = MyIterator(["A", "B", "C"])
    print i.next()
    #A

