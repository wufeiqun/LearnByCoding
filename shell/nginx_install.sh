#!/bin/bash
#owner:rocky
#date:201700908
USER=rocky
GROUP=rocky
DOWN=/home/rocky/software
NGINX=/home/rocky/nginx
FILENAME=nginx-1.12.1
SCRIPT=/home/rocky/script

#first step,check the directory if exist!

if [ ! -x $DOWN ] ;then
	mkdir $DOWN
fi	

if [ ! -x $SCRIPT ] ;then
	mkdir $SCRIPT
fi	

cd $DOWN
wget http://nginx.org/download/$FILENAME.tar.gz
tar -zxf $FILENAME.tar.gz -C
echo "---------------download nginx successfully-------------"
#compile nginx!
cd $DOWN/$FILENAME
./configure \
--prefix=$NGINX \
--sbin-path=$NGINX/sbin/nginx
--conf-path=$NGINX/conf/nginx.conf \
--pid-path=$NGINX/logs/nginx.pid \
--with-http_ssl_module \
--user=$USER \
--group=$GROUP \

make 
make install

#start the nginx with qfpay user.
cd /home/$USER/nginx/sbin
chown root nginx
chmod u+s nginx
echo "--------------------nginx installation successful-------------------------------"

cd $NGINX
mkdir conf.d

