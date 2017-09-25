#!/usr/bin/env python
#coding: utf-8
#修改本机的主机名称为eth0的网卡的IP地址(点转化为了下划线)
import sys
import socket
import fcntl
import struct
import platform
import socket
import subprocess

iface = "eth0"

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def get_sys_version():
    release = platform.release()
    if "el6" in release:
        return "el6"
    elif "el7" in release:
        return "el7"
    else:
        return "unknown"

def change():
    version = get_sys_version()
    ip = get_ip_address(iface)
    ip_new = ip.replace(".", "_")
    if version == "el6":
        subprocess.call(["hostname", ip_new])
        subprocess.call(["cp", "/etc/sysconfig/network", "/tmp/network.bak"])
        with open("/etc/sysconfig/network", "r") as f:
            ret = f.readlines()
            ret[1] = "HOSTNAME={0}\n".format(ip_new)
        with open("/etc/sysconfig/network", "w") as f:
            f.writelines(ret)

    elif version == "el7":
        subprocess.call(["hostnamectl", "--static", "set-hostname", ip_new])
        subprocess.call(["hostnamectl", "set-hostname", ip_new])
    else:
        print("{0} version unknown!".format(ip))


def show():
    ip = get_ip_address("eth0")
    version = get_sys_version()
    ip_new = ip.replace(".", "_")
    print("ip={0}, version={1}, ip_new={2}, hostname={3}".format(ip, version, ip_new, socket.gethostname()))

if __name__ == "__main__":
    change()
    show()
