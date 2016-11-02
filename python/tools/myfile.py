#!/usr/bin/env python
# coding:utf-8
"""
文件上传/下载脚本

使用方法:
    将该文件放到PATH中,并加入alias:
    up='python myfile.py up '
    down='python myfile.py down '

    up filename即可

"""
import sys
import subprocess

UPLOAD_URL = "http://jp.rockywu.me/up/"
DOWNLOAD_URL = "http://jp.rockywu.me/down/"

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    out = p.stdout.readlines()
    return p.returncode, out



if __name__ == "__main__":
    if len(sys.argv) < 3:
        pass
    if sys.argv[1] in ("u", "up"):
        cmd = "curl -T {filename} {url}".format(filename=sys.argv[2], url=UPLOAD_URL)
    elif sys.argv[1] in ("d", "down"):
        cmd = "wget {url}{filename}".format(filename=sys.argv[2], url=UPLOAD_URL)
    run_cmd(cmd)
