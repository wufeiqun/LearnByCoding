#!/usr/bin/env python
# coding:utf-8
from gevent import monkey
monkey.patch_all()

import urllib
import traceback

import requests
from gevent.pool import Pool
from openpyxl import load_workbook

filepath = "huan.xlsx"
ROW = 1000

wb = load_workbook(filename=filepath)
sheets = wb.get_sheet_names()
ws = wb.get_sheet_by_name(sheets[0])

def getBaikeUrl(name):
    """
    获取每一个明星的百度百科的个人页面,从百科里面直接搜索.
    """
    if isinstance(name, unicode):
        name = name.encode("utf-8")
    url = "http://baike.baidu.com/search/word?word={0}".format(name)
    resp = requests.get(url, allow_redirects=False)
    url = resp.headers.get("Location")
    print url
    if "search/none" in url:
        return None
    return url

def main(row):
    try:
        name = ws["B{0}".format(row)].value
    except Exception as e:
        print traceback.print_exc(e)
    try:
        ws["G{0}".format(row)].value = getBaikeUrl(name)
    except Exception as e:
        print traceback.print_exc(e)
    print "已完成第: {0}个.".format(row)

pool = Pool(10)

for row in xrange(1700, 2400):
    pool.spawn(main, row)
    print "第{0}行加入队列!".format(row)
pool.join()

wb.save(filename="huan.xlsx")

