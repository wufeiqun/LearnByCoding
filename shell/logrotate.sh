#!/bin/bash
# nginx日志切割样例, 线上nginx最好使用yum来安装

log_name="access.log"
log_path="/var/log/nginx/"
backup_path="/data/"
pid_path="/var/run/nginx.pid"
# 按天备份日志
#log_name_new="${log_name}_$(date -d "today -1 day" +"%Y%m%d").log"
#按小时备份日志, 日志名字为2018012401的日志包括了1点到2点之间的日志
log_name_new="${log_name}_$(date -d "today -1 hour" +"%Y%m%d%H").log"
# 备份目录不存在的话创建
if [ ! -x "$backup_path" ]; then
  mkdir "${backup_path}"
fi

# 备份
mv ${logs_path}/${log_name} ${backup_path}/${log_name_new}

# 压缩
gzip -f ${backup_path}/${log_name_new}

# nginx重新打印日志
kill -USR1 `cat ${pid_path}`

# 删除历史日志
find ${backup_path} -maxdepth 1 -name "*.gz" -mtime +30 |xargs rm -f
