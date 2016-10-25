#!/usr/bin/env python
# coding:utf-8
"""
统计某一个目录下所有文件的大小,包括目录下所有层次的文件
"""
import os

def count(path):
    for root, dirs, files in os.walk(path):
        for fname in files:
            f = os.path.join(root, fname)
            fsize = os.stat(f).st_size
            print "{0} --->{1} bytes".format(f, fsize)


if __name__ == "__main__":
    path="python"
    count(path)

