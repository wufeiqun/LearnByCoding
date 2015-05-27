#!/usr/bin/env python
#coding=utf-8
# ########################################
# Function:    CMS self-defined monitor SDK
# Usage:       python cms_post.py ali_uid, metric_name, value, fields
# Author:      CMS Dev Team
# Company:     Aliyun Inc.
# Version:     1.0
# Description: Since Python 2.6, please check the version of your python interpreter
# ########################################
import sys
import time
import socket
import random
import urllib
import httplib
import json
import logging
from logging.handlers import RotatingFileHandler

REMOTE_HOST = 'open.cms.aliyun.com'
REMOTE_PORT = 80
REMOTE_MONITOR_URI = "/metrics/put"


def post(ali_uid, metric_name, metric_value, fields):
    # 创建Logger对象,来处理日志记录等工作,name为post.如果不指定name则返回root对象，多次使用相同的name调用getLogger方法返回同一个logger对象。
    logger = logging.getLogger('post')
	#设置日志的级别。对于低于该级别的日志消息将被忽略.
    logger.setLevel(logging.INFO)
	#定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大10M
    handler = RotatingFileHandler(filename="/tmp/aliyun.log", mode='a', maxBytes=10 * 1024 * 1024, backupCount=3)
	#定义日志的格式.'日志的时间','日志级别名称','日志信息'	
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    socket.setdefaulttimeout(10)

    # convert dimensions
    kv_array = fields.split(',')
    dimensions = {}
    for kv in kv_array:
        kv_array = kv.split('=')
        dimensions[kv_array[0]] = kv_array[1]
    json_str = json.dumps(dimensions)

    #current timestamp
    timestamp = int(time.time() * 1000)

    #concate to metrics
    metrics = '[{"metricName": "%s","value": %s, "unit": "None","timestamp": %s, "dimensions": %s}]' % (
        metric_name, metric_value, timestamp, json_str)
    print metrics

    params = {"userId": ali_uid, "namespace": "acs/custom/%s" % ali_uid, "metrics": metrics}

    #report at random 5 seconds
    interval = random.randint(0, 5000)
    time.sleep(interval / 1000.0)

    data = urllib.urlencode(params)
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Connection": "close"}
    exception = None
    http_client = None
    try:
        http_client = httplib.HTTPConnection(REMOTE_HOST, REMOTE_PORT)
        try:
            http_client.request(method="POST", url=REMOTE_MONITOR_URI, body=data, headers=headers)
            response = http_client.getresponse()
            if response.status == 200:
                return
            else:
                print "response code %d, content %s " % (response.status, response.read())
                logger.warn("response code %d, content %s " % (response.status, response.read()))
        except Exception, e:
            exception = e
    finally:
        if http_client:
            http_client.close()
        if exception:
            logger.error(exception)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "illegal argument counts, should be 4"
        exit(1)
    post(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
