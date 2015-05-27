#!/usr/bin/env python
#coding=utf-8
import random

number = random.randint(1,20)
print 'Guess the number!'
running = True
while running:
	num = int( raw_input("Please input a number:"))

	if num < number:
		print 'Your answer is smaller.....'
	elif num > number:
		print 'Your answer is bigger....'
	if num != number:
		continue
	print '恭喜你，答对了！！！'
	break
else:
	print 'Loop is over!'

print 'Done!!!'
	
