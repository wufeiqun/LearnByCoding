# Python API for local hosts
import pprint


class DuplicateKeyError(Exception):
    pass

class Hosts:
    def __init__(self, path="/etc/hosts"):
        self.path = path
        self.ip_map_host = {} # ip和host的对应关系
        self.host_map_ip = {} # host和ip的对应关系
        self.unprocessed = [] # 不可以处理的hosts行, 比如ipv6, 或者注释的行, 这里为了不修改这些内容
        self.host2obj()

    def host2obj(self):
        """
        将hosts文件转换为python对象, 方便操作, 字典,value为set
        {"192.168.1.1": {"rockywu.me", "example.com"}}
        """
        with open(self.path) as f:
            flines = f.readlines()
        flines = [fl.strip() for fl in flines if fl]
        for fline in flines:
            if fline:
                if fline.startswith("#") or fline.startswith("::"):
                    self.unprocessed.append(fline)
                else:
                    ip = fline.strip().split()[0]
                    hosts = fline.strip().split()[1:]
                    # 添加到ip_map_host中
                    if ip in self.ip_map_host:
                        for host in hosts:
                            self.ip_map_host[ip].add(host)
                    else:
                        self.ip_map_host[ip] = set(hosts)
                    # 添加到host_map_ip中
                    for host in hosts:
                        if host not in self.host_map_ip:
                            self.host_map_ip[host] = ip
                        else:
                            print(host)
                            raise DuplicateKeyError()
        pprint.pprint(self.host_map_ip)
        pprint.pprint(self.ip_map_host)

    def set(self, ip, host):
        if ip in self.ip_map_host:
            if host in self.host_map_ip:
                if self.host_map_ip[host] == ip:
                    return
                else:
                    self.ip_map_host[self.host_map_ip[host]].remove(host)
                    self.ip_map_host[ip].add(host)
            else:
                self.ip_map_host[ip].add(host)
        else:
            if host in self.host_map_ip:
                self.ip_map_host[self.host_map_ip[host]].remove(host)
                self.ip_map_host[ip] = set()
                self.ip_map_host[ip].add(host)
            else:
                self.ip_map_host[ip] = set()
                self.ip_map_host[ip].add(host)

    def save(self):
        """保存obj到原hosts文件中"""
        flines = []
        for ip, host in self.ip_map_host.items():
            flines.append(ip + " " + " ".join(host) + "\n")

        with open(self.path, "w") as f:
            f.writelines(flines)
            if self.unprocessed:
                f.writelines(self.unprocessed)


if __name__ == "__main__":
    host = Hosts(path="hosts")
    host.set(ip="192.168.11.51", host="j.rockywu.me")
    host.save()
