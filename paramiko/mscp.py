#!/usr/bin/env python
#coding: utf-8
#批量复制文件到多台远程机器
import os
import threading

import paramiko


class MultiSCP:
    def __init__(self, remote_path, local_path, filename, iplist, username, password=None, port=22):
        self.remote_path = remote_path
        self.local_path = local_path
        self.filename = filename
        self.iplist = iplist
        self.username = username
        self.password = password
        self.port = port

    def get_iplist(self):
        with open(self.iplist) as f:
            iplist = f.readlines()
            iplist = [ip.strip() for ip in iplist]
        return iplist

    def send(self, ip):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.password:
            client.connect(ip, self.port, self.username, self.password, timeout=10)
        else:
            client.connect(ip, self.port, self.username, timeout=10)

        sftp = paramiko.SFTPClient.from_transport(client.get_transport())

        local_path = os.path.join(self.local_path, self.filename)
        remote_path = os.path.join(self.remote_path, self.filename)
        sftp.put(local_path, remote_path)
        print("{0}: {1} 传输完毕!".format(ip, self.filename))

    def run(self):
        threads = []
        iplist = self.get_iplist()
        for ip in iplist:
            print("开始处理服务器: {0}...".format(ip))
            t = threading.Thread(target=self.send, args=(ip,))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    remote_path = "/home/rocky/tmp"
    local_path = "/Users/rocky/tmp"
    filename = "test.txt"
    iplist = "iplist.txt"
    username = "rocky"
    mscp = MultiSCP(remote_path, local_path, filename, iplist, username)
    mscp.run()
