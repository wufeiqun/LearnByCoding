#!/bin/bash 
DATE=`date "+%Y%m%d %H:%M:%S"` 
MYSQL_TAR='/root/software/mysql-5.5.42'
MYSQL_DIR=/home/test/mysql 
RPMLIST="make gcc gcc-c++  autoconf automake  bison bison-devel ncurses ncurses-devel zlib* libxml* libtool-ltdl-devel* cmake"
#create mysql user !
if [[`ls /home|grep test` = test ]];then
 echo "user test is exsit!"
else
 useradd -d /home/test test
fi
#create mysql directory.
cd /home/test
mkdir  mysql mysql/data mysql/etc mysql/tmp mysql/var mysql/log script
chown -R test:test /home/test/


#check and uninstall the old version!
echo  '----------check and uninstall the old version mysql----------'
sleep 1
rpm -qa |grep mysql  > /tmp/mysqlremove.txt 
if [ $? -eq 0 ];then 
for i in $(cat /tmp/mysqlremove.txt); do rpm -e --nodeps $i; done 
echo -e "$DATE \033[32m MYSQL already removed \033[0m" >> /home/test/mysql_install.log 
else
echo -e "$DATE \033[32m MYSQL does not exist \033[0m"  >> /home/test/mysql_install.log
fi 


#install some dependent softwares!
sleep 1

yum -y install $RPMLIST 
rpm -q --qf '%{NAME}-%{VERSION}-%{RELEASE} (%{ARCH})\n' make gcc gcc-c++  autoconf automake  bison bison-devel ncurses ncurses-devel zlib* libxml* libtool-ltdl-devel* cmake

#download the mysql tar file.
cd /root/software
wget http://mirrors.sohu.com/mysql/MySQL-5.5/mysql-5.5.42.tar.gz
#install mysql!
echo '----------解压部分开始----------'
sleep 1
tar -zxvf  $MYSQL_TAR.tar.gz -C /root/software/
echo 'tar -xf already ----> ok'    >> /home/test/mysql_install.log
sleep 5
if [ -d $MYSQL_TAR ];then 
cd $MYSQL_TAR
sleep 2
fi
echo '----------重头戏装包开始----------'
sleep 1
if [ -f $MYSQL_TAR/CMakeCache.txt ]; then
echo 你已经装好了一个数据库顶多是没有执行 请先启动正常使用如有问题执行 ./mysql_install_db --user=test --basedir=/home/test/mysql --datadir=/home/test/mysql/data 执行上一条命令如果还是不行请删除你现有的数据库再执行该脚本 
else
cd $MYSQL_TAR
cmake \
-DCMAKE_INSTALL_PREFIX=/home/test/mysql \
-DMYSQL_DATADIR=/home/test/mysql/data \
-DSYSCONFDIR=/home/test/mysql/etc \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_MEMORY_STORAGE_ENGINE=1 \
-DWITH_READLINE=1 \
-DMYSQL_UNIX_ADDR=/home/test/mysql/tmp/mysql.sock \
-DMYSQL_TCP_PORT=3306 \
-DENABLED_LOCAL_INFILE=1 \
-DWITH_PARTITION_STORAGE_ENGINE=1 \
-DEXTRA_CHARSETS=all \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci

fi

echo '----------start make----------'
sleep 1
make 
sleep 5
echo '----------start make install----------'
sleep 5
make install 

cp $MYSQL_DIR/bin/mysql /usr/bin/
cp $MYSQL_DIR/bin/mysqldump /usr/bin/
cp $MYSQL_DIR/support-files/my-huge.cnf  $MYSQL_DIR/etc/my.cnf
cp $MYSQL_DIR/etc/my.cnf $MYSQL_DIR/etc/my.cnf.bak
/home/test/mysql/scripts/mysql_install_db --user=test --basedir=/home/test/mysql --datadir=/home/test/mysql/data --skip-name-resolve --defaults-file=$MYSQL_DIR/etc/my.cnf 
chown -R test:test /home/test/mysql
#startup the mysqli
echo " #!/bin/bash ">/home/test/script/mysql_start.sh
echo "/home/test/mysql/bin/mysqld --defaults-file=/home/test/mysql/etc/my.cnf &">>/home/test/script/mysql_start.sh
chmod +x /home/test/script/mysql_start.sh
chown -R test:test /home/test
su - test -c bash  /home/test/script/mysql_start.sh
echo "----------mysql successfully installed!----------"
echo "-----Please run the /home/test/mysql/bin/mysql_secure_installation to init mysql!-----"


