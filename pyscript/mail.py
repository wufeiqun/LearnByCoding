#!/usr/bin/env python
#coding=utf-8
#sample of sending mail with python.
import smtplib
from email.mime.text import MIMEText

#定义邮件发送方以及接受方。
sender = '***@126.com'
passwd = '******'
receivers = '******'

#使用MIMEText构造符合smtp协议的header,body.
msg = MIMEText('这是一封神奇的邮件！！！','text','utf-8')
msg['Subject'] = "don't be shy !!"
msg['From'] = sender
msg['To'] = receivers
#连接邮件服务器,登录并发送邮件。
s = smtplib.SMTP("smtp.126.com",timeout=30)
s.login(sender,passwd)
s.sendmail(sender,receivers,msg.as_string())
s.close
