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
import json

import requests

base_url = "http://fanyi.youdao.com/openapi.do?keyfrom=RockyDict&key=1158212758&type=data&doctype=json&version=1.1&only=dict&q="


def main(text):
    if isinstance(text, unicode):
        text = text.encode("utf-8")
    req = requests.get("{0}{1}".format(base_url, text), timeout=5).json()
    if req["errorCode"] == 0:
        if req.has_key("basic"):
            print ",".join(req.get("basic").get("explains"))
    elif req["errorCode"] == 20:
        print "要翻译的文本过长"
    elif req["errorCode"] == 30:
        print "无法进行有效的翻译"
    elif req["errorCode"] == 40:
        print "不支持的语言类型"
    elif req["errorCode"] == 50:
        print "无效的key"
    elif req["errorCode"] == 60:
        print "无词典结果,仅在获取词典结果生效"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])


