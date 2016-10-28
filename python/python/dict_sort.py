#!/usr/bin/env python
#coding=utf-8
#不同的字典排序的方法。
import operator

dicta =  {'rocky':'25','tony':'32','jerry':'26','tom':'26','evil':'23','24':'jk'}
#按照字典的key倒序排序。并输出key的list。
print sorted(dicta,reverse=True)
# ['24', 'evil', 'jerry', 'rocky', 'tom', 'tony']

#按照字典的key顺序排序，并显示整个字典。
print sorted(dicta.iteritems())
#[('24', 'jk'), ('evil', '23'), ('jerry', '26'), ('rocky', '25'), ('tom', '26'), ('tony', '32')]

#按照字典的value进行顺序排序。itemgetter函数可以获取目标的维度，或者换成key=lambda x:d[1],效果相同。从0开始计数。
print sorted(dicta.iteritems(),key=operator.itemgetter(1),reverse=False)
#dict.iteritems() 跟dict.items()区别是，前者返回的是迭代器，后者返回的是字典的元素的list。两者都可以用于循环迭代。
