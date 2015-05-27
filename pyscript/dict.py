#!/usr/bin/env python
#coding=utf-8
import sys
import json
import requests

baseurl = 'http://fanyi.youdao.com/openapi.do?keyfrom=rockyblog&key=1133683542&type=data&doctype=json&version=1.1&q='

result = requests.get(baseurl+sys.argv[1])
try:
	print json.dumps(result.json()['basic']['explains']).decode("unicode-escape")
except: 
	print json.dumps(result.json()['web']).decode("unicode-escape")
