#!/bin/bash

#CONF='shadowsocks.json'
#IP=`grep '"server"' $CONF | awk -F '"' '{print $4}'`
#
#echo '>> server ip :' $IP

echo '>> cleanup'
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
ipset destroy ss_conf

echo '>> create ipset'
ipset create ss_conf hash:net

# curl 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest' | grep ipv4 | grep CN | awk -F\| '{ printf("%s/%d\n", $4, 32-log($5)/log(2)) }' > chnroute.txt
#echo '>> import chnroute to ipset'
for i in $( cat /etc/chinadns_chnroute.txt ) ; do ipset add ss_spec $i ; done

echo '>> create new chain'
iptables -t nat -N SHADOWSOCKS
iptables -t mangle -N SHADOWSOCKS

echo '>> ignore ss server ip'
iptables -t nat -A SHADOWSOCKS -d 118.193.81.214 -j RETURN
iptables -t nat -A SHADOWSOCKS -d 161.202.82.168 -j RETURN

echo '>> ignore ipset ip'
iptables -t nat -A SHADOWSOCKS -m set --match-set ss_conf dst -j RETURN
iptables -t nat -A SHADOWSOCKS -p tcp -j REDIRECT --to-ports 1080

iptables -t nat -A PREROUTING -p tcp -j SHADOWSOCKS
iptables -t mangle -A PREROUTING -j SHADOWSOCKS




