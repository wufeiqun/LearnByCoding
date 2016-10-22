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
```

#### Sort

```
1. 按照年龄倒排
>>> home = [{"name": "Rocky", "age": 26},{"name": "Victor", "age": 24}, {"name": "Father", "age": 53}]
>>> print sorted(home, key=lambda person: person["age"], reverse=True)
[{'age': 53, 'name': 'Father'}, {'age': 26, 'name': 'Rocky'}, {'age': 24, 'name': 'Victor'}]

```
