#!/bin/bash
#auto install python2.7.8 to /usr/local directory!
#and install some libs for python.install virtualenv for all and install supervisor/shadowsocks for root.
#for Centos6.5
#owner:rocky
#date:2015.02.26
#


#mkdir for python software.
SOFT=/root/software

if [ -x "$SOFT" ];then
echo "the directory is exists!!!"
else 
mkdir $SOFT
fi
echo "--------------------mkdir successfully----------------------"
#install the essential libs.some of them is chooseable.gcc is needed.
yum install -y epel-release
yum -y   groupinstall 'Development tools'
yum  -y  install gcc zlib-devel openssl-devel sqlite-devel bzip2-devel  wget
sleep 5
echo "--------------------update system finished!!--------------------"
#download python2.7.8 from source.
cd $SOFT
wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz

#tar and compile python.
tar -zxf Python-2.7.8.tgz
cd Python-2.7.8
./configure --prefix=/usr/local
make 
make install


echo "-------------------compile successfully!!--------------------"

#replace the system default python.
cd /usr/bin
mv python python2.6.6
ln -s /usr/local/bin/python2.7 /usr/bin/python
python -V

#replace the yum python.

sed -i 's/python/python2.6/g' /usr/bin/yum

echo "------------------install python2.7.8 successfully!!!-----------------"

#install virtualenv
cd /root/software
curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-12.0.7.tar.gz
tar xvfz virtualenv-12.0.7.tar.gz
cd virtualenv-12.0.7
python setup.py install
echo "---------------------install virtualenv successful--------------------"

#make virtualenv for shadowsocks and install supervisor.
cd /root
virtualenv shadowsocks
mkdir /root/shadowsocks/etc  /root/shadowsocks/log
source /root/shadowsocks/bin/activate
pip install supervisor
echo "--------------------supervisord installed successfully !!!------------------"

#set supervisor.
echo -e "#!/bin/bash""\n""/root/shadowsocks/bin/supervisorctl -c /root/shadowsocks/etc/supervisord.conf $1 $2" > /root/superctl
chmod +x /root/superctl
cd /root/shadowsocks/etc
cat >supervisord.conf<<EOF

[unix_http_server]
file=/root/shadowsocks/log/supervisor.sock   

[supervisord]
logfile=/root/shadowsocks/log/supervisord.log
logfile_maxbytes=50MB       
logfile_backups=10           
loglevel=info               
pidfile=/root/shadowsocks/log/supervisord.pid
nodaemon=false          
minfds=1024                 
minprocs=200                

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///root/shadowsocks/log/supervisor.sock 

[program:shadowsocks]
command=/usr/bin/ss-server -c /etc/shadowsocks-libev/config.json
user=root

EOF

echo "/root/shadowsocks/bin/supervisord -c /root/shadowsocks/etc/supervisord.conf">/etc/rc.local

echo "-------------------------supervisor settings is ok-------------------------"

#install shadowsocks.
cd /etc/yum.repos.d/
wget https://copr.fedoraproject.org/coprs/librehat/shadowsocks/repo/epel-6/librehat-shadowsocks-epel-6.repo
yum install  shadowsocks-libev  lsof  -y
chkconfig shadowsocks-libev off
cd /etc/shadowsocks-libev
mv config.json config.json.bak
cat >config.json<<EOF
{
    "server":"0.0.0.0",
    "server_port":1234,
    "local_port":5678,
    "password":"helloworld",
    "timeout":300,
    "method":"aes-256-cfb",
    "workers":10
}
EOF

echo "---------------------shadowsocks installed successfully!!!----------------------"

#start supervisor.
/root/shadowsocks/bin/supervisord -c /root/shadowsocks/etc/supervisord.conf

#check the service status.
PORT=`lsof -i:1234|grep -v 'PID'|awk '{print $2}'`
if [ "$PORT" != " " ];then
	echo "Shadowsocks is OK ! enjoy yourself!!!"
else
	echo "Ops,something is wrong,please check it!!!"
fi

exit 0

