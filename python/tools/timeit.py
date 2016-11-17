#!/usr/bin/env python
# coding:utf-8
"""
统计函数运行时间的装饰器
"""
import time

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Finished with {0:.2f}s".format(end-start))
    return wrapper

if __name__ == "__main__":
    @timeit
    def test(name):
        print("Hi, {0}".format(name))

    test("Rocky")
