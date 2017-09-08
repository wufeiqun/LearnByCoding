#!/bin/bash
#install python3.6 to /home/rocky/python3
#for Centos7
#owner:rocky
#date:2017.09

DOWN=/home/rocky/software
PREFIX=/home/rocky/python3
VERSION=3.6.2
URL=https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz

if [  ! -d $DOWN ];then
    mkdir $DOWN
fi

if [  ! -d $PREFIX ];then
    mkdir $PREFIX
fi

cd $DOWN
wget $URL

#tar and compile python.
tar -zxf Python-$VERSION.tgz
cd Python-$VERSION
./configure --prefix=$PREFIX
make && make install

