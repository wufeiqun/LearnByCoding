#!/bin/bash
#This is a script to initialize the centos7 system,just for my flavor,you can modifiy it according your need.

#install epel-release and update.
yum install epel-release -y && yum update -y
yum -y   groupinstall 'Development tools'
yum install gcc gcc-c++ make autoconf automake libtool make pcre-devel openssl-devel bison-devel patch unzip ncurses-devel zlib-devel bzip2-devel  wget readline-devel sqlite-devel telnet nc

#disable selinux
if [ ! -f "/etc/selinux/config" ]; then 
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
fi 
setenforce 0

# stop firewall
systemctl stop firewalld.service
systemctl disable firewalld.service

#change default file decorators
if [ -f "/etc/security/limits.d/20-nproc.conf" ]; then

cat > /etc/security/limits.d/20-nproc.conf << EOF
*           soft   nofile       65535
*           hard   nofile       65535
*           soft   nproc        65535
*           hard   nproc        65535
EOF
else
cat >> /etc/security/limits.conf << EOF
*           soft   nofile       65535
*           hard   nofile       65535
*           soft   nproc        65535
*           hard   nproc        65535
EOF
fi
#stop ctl-alt-del function
rm -f /usr/lib/systemd/system/ctrl-alt-del.target

#system characters
cat > /etc/locale.conf << EOF
LANG="en_US.UTF-8"
EOF

# Set SSHD config

#optimized kenel

#adduser rocky
useradd rocky
chmod +w /etc/sudoers
echo "rocky        ALL=(ALL)NOPASSWD:     ALL" >>/etc/sudoers
chmod -w /etc/sudoers

