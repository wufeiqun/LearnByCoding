# 工作中遇到调用阿里云的接口有请求限制的情况, 每次请求只能发送20个IP地址, 如果我有超过20个的IP地址的话就需要分组请求了
# 这里模拟一下分组的方法

lst = ["number_{0}".format(n) for n in range(1, 95)]

for i in range(0, len(lst) - 1, 20):
    print(lst[i:i+20])
    print("--" * 20)
