#!/bin/bash
#nginx 日志切割，把普通的access日志切割成按日期分割的日志，方便分析，方便存储备份。
#把这个脚本加入定时任务就OK了。

LOG_PATH="/home/discuz/nginx/logs"
DATE=`date  +%Y%m%d`

#移动日志文件，重命名。
mv ${LOG_PATH}/access.log ${LOG_PATH}/access_$DATE.log 

#向nginx进程发送USR1信号，这是重新打开日志文件的信号。
kill -USR1 $(cat $LOG_PATH/nginx.pid)

exit 0
