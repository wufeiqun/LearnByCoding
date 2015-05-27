#!/usr/bin/env python
#coding=utf-8

import re
import collections

text = open('1.log').read()
pat = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}')
listb = re.findall(pat,text)

def count():
	print '总共有', len(listb),'个IP地址。'
#count = collections.Counter()
#for item in listb:
#	count[item]+=1
#print count



def main():
	listb_set = set(listb)
	dicta = {}
	for item in listb_set:
		dicta[item] = listb.count(item)
	return dicta
	
main()

