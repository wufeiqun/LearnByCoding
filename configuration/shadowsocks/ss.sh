#!/bin/sh
#Author: Rocky
#Date: 2016-11-11

CONF='/etc/shadowsocks.json'
IP=`grep '"server"' $CONF | awk -F '"' '{print $4}'`

echo '>>server IP: ' $IP

echo 'create ipset'
ipset create chnset hash:net

echo '>>add chnroute to ipset'
for i in $(cat '/etc/chinadns_chnroute.txt'); do ipset add chnset $i; done

echo '>>create new chain'
iptables -t nat -N SHADOWSOCKS
iptables -t mangle -N SHADOWSOCKS

echo '>>ignore server ip,very important~'
iptables -t nat -A SHADOWSOCKS -d $IP -j RETURN

echo ">>Ignore LANs and any other addresses you'd like to bypass the proxy."
iptables -t nat -A SHADOWSOCKS -d 0.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 10.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 127.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 169.254.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 172.16.0.0/12 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 192.168.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 224.0.0.0/4 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 240.0.0.0/4 -j RETURN

echo 'ignore ipset ips'
iptables -t nat -A SHADOWSOCKS -m set --match-set chnset dst -j RETURN

echo ">>Anything else should be redirected to shadowsocks's local port"
iptables -t nat -A SHADOWSOCKS -p tcp -j REDIRECT --to-ports 1080

echo 'Apply the rules'
iptables -t nat -A OUTPUT -p tcp  -j SHADOWSOCKS
iptables -t mangle -A PREROUTING -j SHADOWSOCKS
