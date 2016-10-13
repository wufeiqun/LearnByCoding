#!/usr/bin/env python
#coding: utf-8
import os
import sys
import time
import atexit
import signal

class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin="/dev/null", stdout="/dev/null", stderr="/dev/null"):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic.
        """
        #调用umask修改子进程的新建文件权限掩码(比如umask是022,那么新建的文件为666-022=644,文件夹为777-022=755)
        #这样子进程就不会受父进程的umask影响了,增加守护进程灵活性
        os.umask(0)
        #创建子进程
        try:
            pid = os.fork()
            #os.fork会创建子进程,如果是在父进程环境中就会返回子进程的pid(一般不为0),如果在子进程的环境中则返回0
            #如果是父进程环境,则让父进程退出,这样的话子进程就会被init托管而不受主进程的影响
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("Fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        #让子进程脱离父进程的环境
        #切换工作目录到根目录,防止占用可卸载的文件系统,也可以换成其它路径
        os.chdir("/")
        #使用getsid创建一个新的会话(一个或多个进程组的集合),组长进程调用该函数会返回-1(报错),非组长进程调用返回进程组id;该进程会变成会话首进程,该进程会变成新进程组
        #的组长进程,该进程没有控制终端,如果之前有,则会被中断;组长进程不能成为新会话首进程，新会话首进程必定会成为组长进程
        os.setsid()
        #在基于 System V的系统中,有人建议此时再次调用fork,并终止父进程,第二个子进程作为父进程继续运行,这样就保证了盖守护进程不会成为会话首进程,
        #会话的领头进程打开一个终端之后, 该终端就成为该会话的控制终端,意思是一个会话只有会话首进程才有可能控制终端;
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)






