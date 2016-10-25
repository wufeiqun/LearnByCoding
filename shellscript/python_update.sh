#!/bin/bash
#auto install python2.7.8 to /usr/local directory!
#and install some libs for python.
#for Centos6.5
#owner:rocky
#date:2015.01.26
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
yum  -y  install gcc zlib-devel openssl-devel  bzip2-devel  wget readline-devel sqlite-devel
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
cd $SOFT
wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-12.1.1.tar.gz#md5=901ecbf302f5de9fdb31d843290b7217
tar -zxvf virtualenv-12.1.1.tar.gz
cd $SOFT/virtualenv-12.1.1
python setup.py install

echo "---------------------install virtualenv successful--------------------"


