#!/usr/bin/env python
#coding=utf-8
#remove the same values of the list.
def rm_same_value(lst):
	i=0
	while i <= len(lst) - 1:
		j = i + 1
		while j <= len(lst) - 1:
			if lst[j] == lst[i]:
				del lst[j]
				j+=1
			else:
				j+=1
		i+=1
		print lst

if __name__ =='__main__':
	lst = [1,2,3,3,2,1]
	rm_same_value(lst)
