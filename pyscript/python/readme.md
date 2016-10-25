### Learn Python By Coding

#### Function

```
# The default values are evaluated at the point of function definition in the defining scope.

i = 5

def func(arg=i):
    print arg

i = 6

func()

will print 5


当使用可变的数据结构作为默认参数时应当注意:
x = []
def func(a, L=x):
    L.append(a)
    return L

print func(1)
print func(2)
print func(3)
print x
[1]
[1, 2]
[1, 2, 3]
[1, 2, 3]
解读:
1. 函数默认参数的定义只在函数定义的时候执行一次,python参数的传递实际上是对象的引用,当参数是一个不可变的对象的时候,比如说字符串,函数会把参数的链接指向那个字符串,所以不管函数在哪执行,默认参数都已经做好引用了,就不会变了;
,如果默认参数是一个可变对象的话当函数定义以后,如例2,L就会引用定义函数时候的那个空数组,函数在下面被执行的时候修改的其实是那个数组,而L只是一个引用,所以就会出现上面的情况,这样的情况不是我们想要的,避免这种情况的办法是不要给函数传递可变的默认参数,
,当传递的参数不是默认参数的时候没有问题,因为每一次都传入一个新的引用:

def func(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L
这样就不会有问题了

2. non-keyword argument after a keyword argument;default argument must follows non-default argument;


# If arguments are not available separately, write the function call with the *-operator to unpack the arguments out of a list or tuple:
>>>args = [3, 6]
>>>range(*args)
[3, 4, 5]

```

*. 求两个长度相同的list个对应元素之和

```
之前比较年轻,使用遍历的笨办法,这次试用map

x, y = range(1, 5), range(5, 9)
map(lambda a,b: a+b, x, y)

[6, 8, 10, 12]
```

*. 列出1-20之间能被3或者5整除的数字
```
def f(x): return x % 3 == 0 or x % 5 == 0
filter(f, range(1, 20))

[3, 5, 9, 10, 12, 15, 18, 20]

```
*. 求一个整数list的所有元素的积
```
reduce(lambda x, y: x*y, [1,2,3,4,5])

120

```
* 列表推导式
```
>>> [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
[(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]
```

* zip使用方法
```
x = ["Rocky", "Victor", "Huan"]
y = [26, 24, 25]
zip(x, y)
[("Rocky", 26), ("Victor", 24), ("Huan", 25)]

dict(zip(x, y))
{"Rocky": 26, "Victor": 24, "Huan": 25}

for k, v in zip(x, y):
    print k, v

Rocky  26
Victor 24
Huan 25

```



#### Sort

```
sorted和list的内置方法sort比较:
1. sorted返回一个新的已经排好序的list而不改变原有的list,sort方法会改变原来的数据,如果源数据不需要的话可以使用sort方法
2. 
3. 从python2.2开始sort和sorted都是稳定的排序


1. 按照年龄倒排
方法一:
>>> home = [{"name": "Rocky", "age": 26},{"name": "Victor", "age": 24}, {"name": "Father", "age": 53}]
>>> print sorted(home, key=lambda person: person["age"], reverse=True)
[{'age': 53, 'name': 'Father'}, {'age': 26, 'name': 'Rocky'}, {'age': 24, 'name': 'Victor'}]

方法二:
>>>from operator import itemgetter
>>>print sorted(home, key=itemgetter("age"), reverse=True)
[{'age': 53, 'name': 'Father'}, {'age': 26, 'name': 'Rocky'}, {'age': 24, 'name': 'Victor'}]


2. 按照列表中字符串所含有的感叹号的数量排序
>>>from operator import methodcaller
>>>messages = ['critical!!!', 'hurry!', 'standby', 'immediate!!']
>>>sorted(messages, key=methodcaller("count", "!"))
['standby', 'hurry!', 'immediate!!', 'critical!!!']

3.体重降序 年龄升序(体重为主,年龄为次)

>>>#有主次的话,先比较次优先级的然后比较主优先级的
>>>home = [["Rocky", 26, 75], ["Victor", 24, 75], ["tony", 32, 70]]
>>>from operator import itemgetter
>>> s = sorted(home, key=itemgetter(1))
>>> s
[['Victor', 24, 75], ['Rocky', 26, 75], ['tony', 32, 70]]
>>> sorted(s, key=itemgetter(2))
[['tony', 32, 70], ['Victor', 24, 75], ['Rocky', 26, 75]]

```

#### data structures

```
# list
1. list append quivalent a[len(a):] = [x]

>>> lst = [1,2,3,4]
>>>lst[len(lst):] = [5,6]
>>>lst
>>>[1,2,3,4,5,6]
>>>lst[:2] = [9,8]
>>>lst
[9,8,3,4,5,6]
>>>del lst[1:4]
>>> lst
[9,5,6]


```
