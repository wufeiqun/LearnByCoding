#!/bin/bash
#This is a script to initialize the centos7 system,just for my flavor,you can modifiy it according your need.

#install epel-release and update.
yum install epel-release -y && yum update -y

#install/update some basic software.
yum install gcc  gcc gcc-c++ make autoconf openssl-devel bison patch unzip ncurses-devel axel

#disable selinux
if [ ! -f "/etc/selinux/config" ]; then 
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
fi 
if [ ! -f "/etc/selinux/config" ]; then 
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
fi 
setenforce 0
service iptables stop
iptables -F

#change default file decorators
cat >> /etc/security/limits.conf << EOF
*           soft   nofile       65535
*           hard   nofile       65535
*           soft   nproc        65535
*           hard   nproc        65535
EOF

#stop ctl-alt-del function
ln -s /dev/null /etc/systemd/system/ctrl-alt-del.target

#system characters
#LANG=zh_CN.UTF-8
#SUPPORTED=zh_CN.UTF-8:zh_CN:zh:en_US.UTF-8:en_US:en
#SYSFONT=lat0-sun16
cat >> /etc/locale.conf << EOF
LANG="en_US.UTF-8"
EOF

#set sshd
sed -i '/^#UseDNS/s/#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/g' /etc/ssh/sshd_config

#optimized kenel
touch /etc/sysctl.d/local.conf
cat >> /etc/sysctl.d/local.conf<< EOF
# max open files
fs.file-max = 51200
# max read buffer
net.core.rmem_max = 67108864
# max write buffer
net.core.wmem_max = 67108864
# default read buffer
net.core.rmem_default = 65536
# default write buffer
net.core.wmem_default = 65536
# max processor input queue
net.core.netdev_max_backlog = 4096
# max backlog
net.core.somaxconn = 4096

# resist SYN flood attacks
net.ipv4.tcp_syncookies = 1
# reuse timewait sockets when safe
net.ipv4.tcp_tw_reuse = 1
# turn off fast timewait sockets recycling
net.ipv4.tcp_tw_recycle = 0
# short FIN timeout
net.ipv4.tcp_fin_timeout = 30
# short keepalive time
net.ipv4.tcp_keepalive_time = 1200
# outbound port range
net.ipv4.ip_local_port_range = 10000 65000
# max SYN backlog
net.ipv4.tcp_max_syn_backlog = 4096
# max timewait sockets held by system simultaneously
net.ipv4.tcp_max_tw_buckets = 5000
# turn on TCP Fast Open on both client and server side
net.ipv4.tcp_fastopen = 3
# TCP receive buffer
net.ipv4.tcp_rmem = 4096 87380 67108864
# TCP write buffer
net.ipv4.tcp_wmem = 4096 65536 67108864
# turn on path MTU discovery
net.ipv4.tcp_mtu_probing = 1

# for high-latency network
net.ipv4.tcp_congestion_control = hybla

# for low-latency network, use cubic instead
# net.ipv4.tcp_congestion_control = cubic

EOF

sysctl -p /etc/sysctl.d/local.conf

#time setting.
echo "*/5 * * * * /usr/sbin/ntpdate asia.pool.ntp.org > /dev/null 2>&1" >> /var/spool/cron/root

#add rocky
useradd rocky
chmod +w /etc/sudoers
echo "$USERNAME        ALL=(ALL)NOPASSWD:     ALL" >>/etc/sudoers
chmod -w /etc/sudoers

