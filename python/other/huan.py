#!/usr/bin/env python
# coding:utf-8
from gevent import monkey
monkey.patch_all()

import json
import urllib
import traceback

import requests
from gevent.pool import Pool
from openpyxl import load_workbook


def get_baike_url(name):
    """
    获取每一个明星的百度百科的个人页面,从百科里面直接搜索.
    """
    if isinstance(name, unicode):
        name = name.encode("utf-8")
    url = "http://baike.baidu.com/search/word?word={0}".format(name)
    resp = requests.get(url, allow_redirects=False)
    url = resp.headers.get("Location") if not "search/none" in resp.headers.get("Location") else None
    return url


class Actor(object):
    def __init__(self):
        self.file_name = "huan.xlsx"
        self.work_book = load_workbook(filename=self.file_name)
        self.sheets = self.work_book.get_sheet_names()
        self.work_sheet = self.work_book.get_sheet_by_name(self.sheets[0])

    def tv(self, row):
        try:
            tv_name = []
            for col in ["L", "M", "N", "O"]:
                col_name = self.work_sheet["{0}{1}".format(col, row)].value
                if col_name:
                    tv_name.extend(col_name.split(","))
            tv_name = list(set(tv_name))
            print json.dumps(tv_name, encoding="utf-8", ensure_ascii=False)
        except Exception as e:
            print traceback.print_exc(e)
        #try:
        #    ws["E{0}".format(row)].value = getBaikeUrl(name)
        #except Exception as e:
        #    print traceback.print_exc(e)
        #print "已完成第: {0}个.".format(row)


actor =Actor()

def main():
    pool = Pool(10)
    for row in xrange(2, 5):
        pool.spawn(actor.tv, (row))
        print "第{0}行加入队列!".format(row)
    pool.join()
    #wb.save(filename="huan.xlsx")


if __name__ == "__main__":
    main()
