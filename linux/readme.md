### Linux常用命令

* Linux Performance Tools

![linux performance tools](https://raw.githubusercontent.com/hellorocky/blog/master/picture/4.operation-command.png)
![linux performance tools2](https://raw.githubusercontent.com/hellorocky/blog/master/picture/5.linux_perf_tools_full.png)

* 利用mv进行日志切割

```bash
#/bin/bash
#在python多进程程序中,如果使用自带的log进行日志切割的话,就会出现日志丢失的问题,因为多个进程同时进行切割日志的话会覆盖之前的日志文件,因为名字都相同,最后只剩下一份日志...
#这里说的是每天切割一次

LOG_PATH=/home/rocky/test/python

YESTERDAY=$(date --date="yesterday" +%Y-%m-%d)

mv ${LOG_PATH}/t.py ${LOG_PATH}/t.py.${YESTERDAY}

```
