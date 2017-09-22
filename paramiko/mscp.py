#!/home/jumpserver/python3/bin/python3
#从多台远程机器上传输相同目录的文件到本地, 并且重命名,为了区分哪一个机器来的, 命名规则为文件名字前边加上IP地址

import os
import threading

import paramiko


class MultiSCP:
    def __init__(self, remote_path, local_path, filename, iplist, username, port=22):
        self.remote_path = remote_path
        self.local_path = local_path
        self.filename = filename
        self.iplist = iplist
        self.username = username
        self.port = port

    def get_iplist(self):
        with open(self.iplist) as f:
            iplist = f.readlines()
            iplist = [ip.strip() for ip in iplist]
        return iplist

    def copy_to_local(self, ip):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, self.port, self.username)

        sftp = paramiko.SFTPClient.from_transport(client.get_transport())

        cmd = "find {0} -type f -name {1}".format(self.remote_path, self.filename)
        stdin, stdout, stderr = client.exec_command(cmd)
        out, err = stdout.readlines(), stderr.read()
        if err:
            print("{0}遇到了点问题: {1}".format(ip, err))
        else:
            for abs_fname in out:
                abs_fname = abs_fname.strip()
                fname = os.path.basename(abs_fname)
                new_fname = "{0}_{1}".format(ip, fname)
                nf_local_path = os.path.join(local_path, new_fname)
                sftp.get(abs_fname, nf_local_path)
                print("{0} 传输完毕!".format(new_fname))

    def run(self):
        threads = []
        iplist = self.get_iplist()
        for ip in iplist:
            print("开始处理服务器: {0}...".format(ip))
            t = threading.Thread(target=self.copy_to_local, args=(ip,))
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    remote = "/home/xxx/applogs/app_stat/dpool/miaopai_*_20170915*.log.gz"
    remote_path = os.path.dirname(remote)
    local_path = "/home/xxx/bigdata/20170915"
    filename = os.path.basename(remote)
    iplist = "/home/xxx/iplist.txt"
    #iplist = "test.txt"
    username = "xxx"
    port = 22
    mscp = MultiSCP(remote_path, local_path, filename, iplist, username)
    mscp.run()
