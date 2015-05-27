#coding=utf-8
import os
import shutil 
from fabric.api import *

#定义主机组,优先级高于den.hosts.方便后面使用装饰器调用.
env.roledefs={
	'test':['qfpay@172.100.102.102']
	'mos':['qfpay@106.3.39.237']
}

env.GIT_SERVER = 'git.qfpay.net'  # ssh地址只需要填：git.qfpay.net
env.PROJECT = 'hellorocky' #项目名称.
env.PROJECT_OWNER = 'rocky' #项目主人.
env.DEFAULT_BRANCH = 'master' #默认分支
env.LOCAL_DIR = '/home/zzzz/deploy/docker'
env.TARGET_DIR = '/home/qfpay'

def clone():

	'''
	这一步实现项目代码的克隆.
	port : 映射到宿主机上的端口地址.保证不重复,回头写个脚本判断空闲可用的端口.
	gitname : 项目在git中的名称,比如,git@git.qfpay.net:rocky/hellorocky.git这个项目,直接写rocky/hellorocky
			就行了.
	'''

	project_name = env.PROJECT_OWNER+'/'+env.PROJECT
	gitcmd = 'git clone -b {branch} git@{server}:{name}'.format(branch=env.DEFAULT_BRANCH, server=env.GIT_SERVER, name=project_name)
	tarcmd = "'tar -zcvf '+env.PROJECT+'.tar.gz '+env.PROJECT"
	rmcmd = "'rm -rf '+env.PROJECT+'&& rm -rf '+env.PROJECT+'.tar.gz'"

	with lcd(env.LOCAL_DIR):
		local(gitcmd)
		local(tarcmd)
		put(env.PROJECT+'.tar.gz',env.TARGET_DIR)
		local(rmcmd)

def build(tag):
	'''
	这一步实现docker镜像的创建.

	tag : docker镜像的标签,格式为rocky/docker:1.6
	docker build 常用参数:
	--rm=true 删除构建过程中产生的碎片容器比如名称为None的容器.默认为true.
	'''
	untarcmd = "'tar -zxvf '+env.PROJECT+'.tar.gz'"

	with cd(env.TARGET_DIR):
		run(untarcmd)
		run('docker build -t '+tag+' '+env.PROJECT)
		print 'docker img build successfull !'

def run(port,tag):
	'''
	这一步是run docker的镜像并指定一些run的参数.
	port : 端口映射参数.格式为<host port:container port>
	name : 容器实例的名称,方便区别操作.

	当利用 docker run 来创建容器时，Docker 在后台运行的标准操作包括：
		检查本地是否存在指定的镜像，不存在就从公有仓库下载
		利用镜像创建并启动一个容器
		分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
		从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
		从地址池配置一个 ip 地址给容器
		执行用户指定的应用程序
		执行完毕后容器被终止
	常用的参数:
	-d 后台运行,可以使用docker exec -it <ID> /bin/bash 进入后台运行的容器.
	--name 指定运行实例的名称,方便后续的控制操作,比如删除,停止等.建议带有版本概念.
	-p 端口映射 格式 host port:container port	
	-i 交互
	-t 终端
	如果在使用Docker时有自动化的需求，你可以将containerID输出到指定的文件中（PIDfile），类似于某些应用程序将自身ID输出到文件中，方便后续脚本操作。
	--cidfile="": Write the container ID to the file
	
	''' 
	runcmd = "'docker run -d -p '+port+'--name '+name+tag"
	run(runcmd)
	print 'container created successfully !'
