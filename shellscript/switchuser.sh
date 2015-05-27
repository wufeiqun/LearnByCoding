#!/bin/bash
#this is a script to test the swichuser function.
#一般可以用在开机启一些非root用户的进程，比如supervisor.
whoami

su - qfpay <<!
whoami
!
whoami

