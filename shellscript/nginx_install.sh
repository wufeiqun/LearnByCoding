#!/bin/bash
#owner:rocky
#date:20150129
#auto install nginx for qfpay!
#nginx version 1.2.6
USER=qfpay
GROUP=qfpay
SOFT=/root/software
NGINX=/home/qfpay/nginx


#first step,check the directory if exist!

if [ ! -x $SOFT ] ;then
	mkdir $SOFT
fi	
cd $SOFT
wget http://nginx.org/download/nginx-1.6.2.tar.gz
tar -zxvf nginx-1.6.2.tar.gz -C /root/software/
echo "---------------download nginx successfully-------------"
#install some dependency packeges.
yum -y install gcc automake autoconf libtool make gcc-c++ pcre pcre-devel zlib-devel openssl openssl-devel
echo "-------------dependendenycis installed successful-------------"
#compile nginx!
cd $SOFT/nginx-1.6.2
./configure \
--prefix=$NGINX \
--sbin-path=$NGINX/sbin/nginx
--conf-path=$NGINX/conf/nginx.conf \
--pid-path=$NGINX/logs/nginx.pid \
--with-http_ssl_module \
--with-http_stub_status_module \
--user=$USER \
--group=$GROUP \

make 
make install
mkdir /home/$USER/script
echo -e "#!/bin/bash""\n""/home/user/nginx/sbin/nginx -c /home/user/nginx/conf/nginx.conf" >/home/$USER/script/nginx_start.sh
sed -i s/user/$USER/g /home/$USER/script/nginx_start.sh
chmod +x /home/$USER/script/nginx_start.sh
chown -R $USER.$GROUP /home/$USER/

#start the nginx with qfpay user.
cd /home/$USER/nginx/sbin
chown root nginx
chmod u+s nginx
echo "--------------------nginx installation successful-------------------------------"


