#!/usr/bin/env python
# coding:utf-8
"""
命令行版有道翻译
API key = 1158212758
keyfrom = RockyDict

使用方法:
    将文件dict.py改名为dict并放在当前用户的$PATH中即可.
    $dict hi
    $你好
    $dict 你好
    $hi
"""
import sys
import requests

base_url = "http://fanyi.youdao.com/openapi.do?keyfrom=RockyDict&key=1158212758&type=data&doctype=json&version=1.1&only=dict&q="


def main(text):
    if len(text) > 200:
        return None
    if isinstance(text, unicode):
        text = text.encode("utf-8")
    req = requests.get("{0}{1}".format(base_url, text), timeout=5)
    return req.content


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print main(sys.argv[1])

