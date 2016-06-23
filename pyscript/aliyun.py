#!/usr/bin/env python
#coding:utf-8
#########################################
# Function:    sample linux performance indices
# Usage:       python sampler.py
# Author:      CMS DEV TEAM
# Company:     Aliyun Inc.
# Version:     1.1
#########################################
import os
import os.path
import sys
import time
import operator
import httplib
import logging
import socket
import random
from shutil import copyfile
from subprocess import Popen, PIPE
from logging.handlers import RotatingFileHandler

def network_io_kbitps():
    """Return network I/O statistics for every network interface
    installed on the system as a dict of raw tuples.
    """
    f1 = open("/proc/net/dev", "r")
    try:
        lines1 = f1.readlines()
    finally:
        f1.close()

    retdict1 = {}
    for line1 in lines1[2:]:
        colon1 = line1.find(':')
        assert colon1 > 0, line1
        name1 = line1[:colon1].strip()
        fields1 = line1[colon1 + 1:].strip().split()
        bytes_recv1 = float('%.4f' % (float(fields1[0]) * 0.0078125))
        bytes_sent1 = float('%.4f' % (float(fields1[8]) * 0.0078125))
        retdict1[name1] = (bytes_recv1, bytes_sent1)
    time.sleep(1)
    f2 = open("/proc/net/dev", "r")
    try:
        lines2 = f2.readlines()
    finally:
        f2.close()
    retdict2 = {}
    for line2 in lines2[2:]:
        colon2 = line2.find(':')
        assert colon2 > 0, line2
        name2 = line2[:colon2].strip()
        fields2 = line2[colon2 + 1:].strip().split()
        bytes_recv2 = float('%.4f' % (float(fields2[0]) * 0.0078125))
        bytes_sent2 = float('%.4f' % (float(fields2[8]) * 0.0078125))
        retdict2[name2] = (bytes_recv2, bytes_sent2)
    retdict = merge_with(retdict2, retdict1)
    return retdict

def disk_io_Kbps():
    iostat = Popen("iostat -d -k 1 2 | sed '/Device\|Linux\|^$/d' > /tmp/disk_io", shell=True, stdout=PIPE, stderr=PIPE)
    iostat_error = iostat.communicate()[1].strip()
    if iostat_error:
        logger.error("iostat not exists, %s" % iostat_error)
        return None

    retdict = {}
    exception = None
    try:
        try:
            f = open('/tmp/disk_io', 'r')
        except Exception, ex:
            exception = ex
            logger.error(exception)
        if exception:
            return None
        lines = f.readlines()
        for line in lines:
            name, _, readkps, writekps, _, _, = line.split()
            if name:
                readkps = float(readkps)
                writekps = float(writekps)
                retdict[name] = (readkps, writekps)
        return retdict
    finally:
        f.close()

def merge_with(d1, d2, fn=lambda x, y: tuple(map(operator.sub, x, y))):
    res = d1.copy() # "= dict(d1)" for lists of tuples
    for key, val in d2.iteritems(): # ".. in d2" for lists of tuples
        try:
            res[key] = fn(res[key], val)
        except KeyError:
            res[key] = val
    return res

def get_load():
    try:
        f = open('/proc/loadavg', 'r')
        tmp = f.readline().split()
        lavg_1 = float(tmp[0])
        lavg_5 = float(tmp[1])
        lavg_15 = float(tmp[2])
        f.close()
    except:
        return None
    return lavg_1, lavg_5, lavg_15

def get_tcp_status():
    check_cmd = "command -v ss"
    check_proc = Popen(check_cmd, shell=True, stdout=PIPE)
    ss = check_proc.communicate()[0].rstrip('\n')
    if ss:
        cmd = "ss -ant | awk '{if(NR != 1) print $1}' | awk '{state=$1;arr[state]++} END{for(i in arr){printf \"%s=%s \", i,arr[i]}}' | sed 's/-/_/g' | sed 's/ESTAB=/ESTABLISHED=/g' | sed 's/FIN_WAIT_/FIN_WAIT/g'"
    else:
        cmd = "netstat -anp | grep tcp | awk '{print $6}' | awk '{state=$1;arr[state]++} END{for(i in arr){printf \"%s=%s \", i,arr[i]}}' | tail -n 1"
    tcp_proc = Popen(cmd, shell=True, stdout=PIPE)
    tcp_status = tcp_proc.communicate()[0].rstrip('\n')
    return tcp_status

def get_proc_number():
    cmd = "ps axu | wc -l | tail -n 1"
    proc_func = Popen(cmd, shell=True, stdout=PIPE)
    proc_number = proc_func.communicate()[0].rstrip('\n')
    return proc_number

def all_index():
    return (
        int(time.time() * 1000),
        get_cpu_time(),
        get_mem_usage_percent(),
        check_disk(),
        disk_io_Kbps(),
        network_io_kbitps(),
        get_load(),
        get_tcp_status(),
        get_proc_number()
    )

def collector():
    timestamp, cpu, mem, disk, disk_io, net, load, tcp_status, process_number = all_index()
    disk_utilization = ''
    disk_io_read = ''
    disk_io_write = ''
    internet_networkrx = ''
    internet_networktx = ''
    tcp_status_count = ''
    period_1 = ''
    period_5 = ''
    period_15 = ''

    if UUID:
        cpu_utilization = 'vm.CPUUtilization ' + str(timestamp) + ' ' + str(cpu) + ' ns=ACS/ECS unit=Percent instanceId=%s\n' % UUID

        memory_utilization = 'vm.MemoryUtilization ' + str(timestamp) + ' ' + str(mem[0]) + ' ns=ACS/ECS unit=Percent instanceId=%s\n' % UUID

        if load:
            period_1 = 'vm.LoadAverage ' + str(timestamp) + ' ' + str(load[0]) + ' ns=ACS/ECS unit=count' + ' instanceId=%s period=1min\n' % UUID
            period_5 = 'vm.LoadAverage ' + str(timestamp) + ' ' + str(load[1]) + ' ns=ACS/ECS unit=count' + ' instanceId=%s period=5min\n' % UUID
            period_15 = 'vm.LoadAverage ' + str(timestamp) + ' ' + str(load[2]) + ' ns=ACS/ECS unit=count' + ' instanceId=%s period=15min\n' % UUID

        if disk:
            for name, value in disk.items():
                disk_utilization = disk_utilization + 'vm.DiskUtilization ' + str(timestamp) + ' ' + str(value[0]) + ' ns=ACS/ECS unit=Percent instanceId=%s mountpoint=%s\n' % (UUID, name)

        if disk_io:
            for name, value in disk_io.items():
                disk_io_read = disk_io_read + 'vm.DiskIORead ' + str(timestamp) + ' ' + str(value[0]) + ' ns=ACS/ECS unit=Kilobytes/Second instanceId=%s diskname=%s\n' % (UUID, name)
                disk_io_write = disk_io_write + 'vm.DiskIOWrite ' + str(timestamp) + ' ' + str(value[1]) + ' ns=ACS/ECS unit=Kilobytes/Second instanceId=%s diskname=%s\n' % (UUID, name)

        for name, value in net.items():
            internet_networkrx = internet_networkrx + 'vm.InternetNetworkRX ' + str(timestamp) + ' ' + str(value[0]) + ' ns=ACS/ECS unit=Kilobits/Second instanceId=%s netname=%s\n' % (UUID, name)
            internet_networktx = internet_networktx + 'vm.InternetNetworkTX ' + str(timestamp) + ' ' + str(value[1]) + ' ns=ACS/ECS unit=Kilobits/Second instanceId=%s netname=%s\n' % (UUID, name)

        if tcp_status:
            status_count = tcp_status.split()
            for element in status_count:
                key_value = element.split('=')
                tcp_status_count = tcp_status_count + 'vm.TcpCount ' + str(timestamp) + ' ' + key_value[1] + ' ns=ACS/ECS unit=Count instanceId=%s state=%s\n' % (UUID, key_value[0])

        process_count = 'vm.ProcessCount ' + str(timestamp) + ' ' + process_number + ' ns=ACS/ECS unit=Count instanceId=%s\n' % UUID
    else:
        cpu_utilization = 'vm.CPUUtilization ' + str(timestamp) + ' ' + str(cpu) + ' ns=ACS/ECS unit=Percent\n'

        memory_utilization = 'vm.MemoryUtilization ' + str(timestamp) + ' ' + str(mem[0]) + ' ns=ACS/ECS unit=Percent\n'

        if load:
            period_1 = 'vm.LoadAverage ' + str(timestamp) + ' ' + str(load[0]) + ' ns=ACS/ECS unit=count period=1min\n'
            period_5 = 'vm.LoadAverage ' + str(timestamp) + ' ' + str(load[1]) + ' ns=ACS/ECS unit=count period=5min\n'
            period_15 = 'vm.LoadAverage ' + str(timestamp) + ' ' + str(load[2]) + ' ns=ACS/ECS unit=count period=15min\n'

        if disk:
            for name, value in disk.items():
                disk_utilization = disk_utilization + 'vm.DiskUtilization ' + str(timestamp) + ' ' + str(value[0]) + ' ns=ACS/ECS unit=Percent mountpoint=%s\n' % name

        if disk_io:
            for name, value in disk_io.items():
                disk_io_read = disk_io_read + 'vm.DiskIORead ' + str(timestamp) + ' ' + str(value[0]) + ' ns=ACS/ECS unit=Kilobytes/Second diskname=%s\n' % name
                disk_io_write = disk_io_write + 'vm.DiskIOWrite ' + str(timestamp) + ' ' + str(value[1]) + ' ns=ACS/ECS unit=Kilobytes/Second diskname=%s\n' % name

        for name, value in net.items():
            internet_networkrx = internet_networkrx + 'vm.InternetNetworkRX ' + str(timestamp) + ' ' + str(value[0]) + ' ns=ACS/ECS unit=Kilobits/Second netname=%s\n' % name
            internet_networktx = internet_networktx + 'vm.InternetNetworkTX ' + str(timestamp) + ' ' + str(value[1]) + ' ns=ACS/ECS unit=Kilobits/Second netname=%s\n' % name

        if tcp_status:
            status_count = tcp_status.split()
            for element in status_count:
                key_value = element.split('=')
                tcp_status_count = tcp_status_count + 'vm.TcpCount ' + str(timestamp) + ' ' + key_value[1] + ' ns=ACS/ECS unit=Count state=%s\n' % key_value[0]

        process_count = 'vm.ProcessCount ' + str(timestamp) + ' ' + process_number + ' ns=ACS/ECS unit=Count\n'

    data_post = cpu_utilization + memory_utilization + period_1 + period_5 + period_15 + disk_utilization + disk_io_read + disk_io_write + internet_networkrx + internet_networktx + tcp_status_count + process_count
    print data_post
    interval = random.randint(0, 5000)
    time.sleep(interval / 1000.0)

    headers = {"Content-Type": "text/plain", "Accept": "text/plain"}
    exception = None
    http_client = None
    try:
        try:
            http_client = httplib.HTTPConnection(REMOTE_HOST, REMOTE_PORT)
            http_client.request(method="POST", url=REMOTE_MONITOR_URI, body=data_post, headers=headers)
            response = http_client.getresponse()
            if response.status == 200:
                return
            else:
                logger.warn("response code %d" % response.status)
                logger.warn("response code %s" % response.read())
        except Exception, ex:
            exception = ex
    finally:
        if http_client:
            http_client.close()
        if exception:
            logger.error(exception)

if __name__ == '__main__':
    REMOTE_HOST = 'open.cms.aliyun.com'
    REMOTE_PORT = 80

    # get report address
    if not os.path.isfile("../cmscfg"):
        pass
    else:
        props = {}
        prop_file = file("../cmscfg", 'r')
        for line in prop_file.readlines():
            kv = line.split('=')
            props[kv[0].strip()] = kv[1].strip()
        prop_file.close()
        if props.get('report_domain'):
            REMOTE_HOST = props.get('report_domain')
        if props.get('report_port'):
            REMOTE_PORT = props.get('report_port')

    # get uuid
    if not os.path.isfile("../aegis_quartz/conf/uuid"):
        pass
    else:
        uuid_file = file("../aegis_quartz/conf/uuid", 'r')
        UUID = uuid_file.readline()
        UUID = UUID.lower()

    REMOTE_MONITOR_URI = "/metrics/putLines"
    MONITOR_DATA_FILE_DIR = "/tmp"
    LOG_FILE = "/tmp/" + "vm.log"
    LOG_LEVEL = logging.INFO
    LOG_FILE_MAX_BYTES = 1024 * 1024
    LOG_FILE_MAX_COUNT = 3
    logger = logging.getLogger('sampler')
    logger.setLevel(LOG_LEVEL)
    handler = RotatingFileHandler(filename=LOG_FILE, mode='a', maxBytes=LOG_FILE_MAX_BYTES,
                                  backupCount=LOG_FILE_MAX_COUNT)
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    socket.setdefaulttimeout(10)

    try:
        collector()
    except Exception, e:
        logger.error(e)
        sys.exit(1)
