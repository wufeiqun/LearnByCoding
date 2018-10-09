import ssl
import socket
import datetime

import OpenSSL

#检查指定域名的HTTPS过期时间
#项目依赖安装:
#pip install pyopenssl


def get_server_certificate(hostname, port=443):
    cert=ssl.get_server_certificate((hostname, port))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    expire_date_str = x509.get_notAfter().decode()[:-1]  # 20181107235959Z, 去掉最后的字母Z
    expire_date = datetime.datetime.strptime(expire_date_str, "%Y%m%d%H%M%S")
    expire_date = expire_date + datetime.timedelta(hours=8)  # 默认的时间是0时区的时间, 需要加8个小时
    print(hostname, expire_date)


lines = open("domain.txt").readlines()
for line in lines:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1)
        # 这里检查目标IP地址的443端口是通的, 然后再往下执行
        if client.connect_ex(("{0}".format(line.strip()), 443)) == 0:
            get_server_certificate("{0}".format(line.strip()))
    except socket.gaierror:
        pass
