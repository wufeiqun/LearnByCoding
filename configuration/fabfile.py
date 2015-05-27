#!/usr/bin/env python
#coding=utf-8
import os 
import sys
from fabric.api import local,lcd


if sys.argv[1] in ['-h','--help']:
	print '''
用法:fab push:'script name','comment of the script'
'''
pwd = os.getcwd()
def push(name,commit):
	with lcd(pwd):
		local('git pull')
		local('git add "%s"' % (name))
		local('git commit -m "%s"' % (commit))
		local('git push')
		print 'Push successfully!!!'
