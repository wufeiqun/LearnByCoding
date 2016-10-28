#!/usr/bin/env python
#coding: utf-8
#通过判断网页中是否含有"m3u8"字符来判断请求的是单集还是系列视频
import os
import sys
import re
import json
import urllib
import requests
from bs4 import BeautifulSoup as bs

save_path = os.environ["HOME"] + "/Downloads/"

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "",
        "DNT": 1,
        "Host": "open.163.com",
        "Pragma": "no-cache",
        "Referer": "http://open.163.com/",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
        }


class Downloader(object):
    def __init__(self, url):
        self.url = url
        resp = requests.get(self.url, headers=headers, timeout=10)
        self.soup = bs(resp.text, "lxml")
        if "m3u8" in resp.text:
            self.single = True
        else:
            self.single = False

    def mkPlaylistDir(self):
        '''
        获得系列课程的英文名称并创建本地目录
        '''
        if not self.single:
            if self.url.endswith("html"):
                dirname = self.url.split("/")[-1].split(".")[0]
            else:
                dirname = self.url.split("/")[-2]
            self.dirname = dirname
            try:
                os.mkdir(save_path+dirname)
                print "**" * 20 + "{dirname}已经创建".format(dirname=dirname) + "**" * 20
            except:
                print "目录已经存在!"

    def getUrlList(self):
        '''
        获取系列课程中每一集的名称和视频链接
        return:
        [{url:xxx, title:xxx}, {url:xxx, title:xxx}, ...]
        '''
        self.urlist = []
        if self.single:
            link = {}
            link["title"] = self.soup.find(class_="sname").get_text()
            link["url"]   = self.url
            self.urlist.append(link)
        else:
            table = self.soup.find_all(class_="m-clist", attrs={"style": ""})
            tbody = table[0].find_all(class_="u-ctitle")
            for tr in tbody:
                link = {}
                link["title"] = tr.get_text().replace("\n", "").replace(" ", "")
                link["url"]   = tr.a.get("href")
                self.urlist.append(link)

    def getVideo(self):
        for li in self.urlist:
            resp = requests.get(li["url"], headers=headers, timeout=10)
            title = li["title"] + ".mp4"
            url_pattern = re.compile(r"http://mov.bn.netease.com.+?m3u8")
            url_match = url_pattern.search(resp.text)
            if url_match:
                mp4url = url_match.group().replace("m3u8", "mp4")
                print u"*************************************即将下载 {filename}***********************************".format(filename=title)
                if self.single:
                    ret = urllib.urlretrieve(mp4url, save_path + title)
                else:
                    ret = urllib.urlretrieve(mp4url, save_path+self.dirname+"/"+title)
                print u"************************************{filename} 下载完成!************************************".format(filename=title)
            else:
                print "未匹配到任何视频链接地址!"


if __name__ == "__main__":
    input_url = raw_input("请输入一个网易公开课的链接(单集链接或者课程链接): ")

    if not input_url:
        print "请输入一个有效的链接!"
        sys.exit(1)

    d = Downloader(input_url)
    d.mkPlaylistDir()
    d.getUrlList()
    d.getVideo()
