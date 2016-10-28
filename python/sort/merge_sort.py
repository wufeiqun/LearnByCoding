#!/usr/bin/env python
# coding:utf-8
from collections import deque

#方法一:
def merge_sort_A(lst):
    if len(lst) <= 1:
        return lst

    def merge(left, right):
        merged, left, right = deque(), deque(left), deque(right)
        while left and right:
            merged.append(left.popleft() if left[0] <= right[0] else right.popleft()) # deque popleft is O(1)
        merged.extend(right if right else left)
        return list(merged)

    middle = int(len(lst) // 2)
    left = merge_sort_A(lst[:middle])
    right = merge_sort_A(lst[middle:])
    return merge(left, right)

#方法二
#使用标准库heapq中的merge方法
from heapq import merge

def merge_sort_B(lst):
    if len(lst) <= 1:
        return lst

    middle = int(len(lst) // 2)
    left = merge_sort_B(lst[:middle])
    right = merge_sort_B(lst[middle:])
    return list(merge(left, right))


if __name__ == "__main__":
    lst = [9,8,7,6,5,4,3,2,1]
    print merge_sort_A(lst)
    print merge_sort_B(lst)
