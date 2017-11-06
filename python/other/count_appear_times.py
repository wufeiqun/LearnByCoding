#使用不同的办法来统计列表中对象的出现次数。
import collections


global_list = [1,2,3,4,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,4,4,4]
def way1():
	list1 = set(global_list) #list1是另外一个列表，里面的内容是global_list里面的无重复项.
	for item in list1:
		print(item,'出现了',global_list.count(item),'次')
way1()

#利用dict的特性。
def way2():
	list2 = set(global_list)
	dict2 = {}
	for item in list2:
		dict2[item] = global_list.count(item)
	print(dict2)

way2()

#利用python第三方模块collections.
def way3():
	print(collections.Counter(global_list))
way3()
