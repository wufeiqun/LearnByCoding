#!/usr/bin/env python
#coding:utf-8
'''
得到n个相同长度list的对应位置的和后的list.
比如:
a = [1,2,3,4]
b = [5,6,7,8]
求两个list的和.
结果为:
c = [6,8,10,12]
'''

def add_list(*lsts):
    merged_list = []
    for i in xrange(len(lsts[0])):
        merged_list.append(sum([lst[i] for lst in lsts]))
    return merged_list

if __name__ == '__main__':
    a = [1,2,3,4]
    b = [5,6,7,8]
    print add_list(a,b)
    c = [a,b]
    print add_list(*c)


