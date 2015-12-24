#!/home/qfpay/python/bin/python
#coding=utf-8
#使用方法:把这个脚本放到跟你要使用该邮件的脚本相同目录,然后直接from sendmail import send_mail,直接使用该函数即可.
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time, datetime, types
import traceback, copy
import logging
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.utils import COMMASPACE,formatdate
import smtplib

class MailMessage:
    def __init__(self, subject, fromaddr, toaddr, content):
        self.mailfrom = fromaddr
        self.mailto = toaddr

        self.msg = MIMEMultipart()
        self.msg['From'] = fromaddr
        if type(subject) == types.UnicodeType:
            self.msg['Subject'] = '=?UTF-8?B?%s?=' % (base64.b64encode(subject.encode('utf-8')))
        else:
            self.msg['Subject'] = '=?UTF-8?B?%s?=' % (base64.b64encode(subject))

        if type(toaddr) in (types.TupleType, types.ListType):
            self.msg['To'] = COMMASPACE.join(toaddr)
        else:
            self.msg['To'] = toaddr
        self.msg['Date'] = formatdate(localtime=True)
        if content.find('<') > 0 and content.find('>') > 0:
            self.msg.attach(MIMEText(content, 'html', 'utf-8'))
        else:
            self.msg.attach(MIMEText(content, 'plain', 'utf-8'))

    def append_file(self, filename, conttype):
        maintype, subtype = conttype.split('/')
        part = MIMEBase(maintype, subtype)
        part.set_payload(open(filename, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="你好.txt"' % os.path.basename(filename))
        self.msg.attach(part)

    def append_file_data(self, filename, data, conttype):
        maintype, subtype = conttype.split('/')
        part = MIMEBase(maintype, subtype)
        part.set_payload(data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))
        self.msg.attach(part)


    def append_data(self, content, conttype):
        maintype, subtype = conttype.split('/')
        part = MIMEBase(maintype, subtype)
        part.set_payload(content)
        encoders.encode_base64(part)
        self.msg.attach(part)

    def tostring(self):
        return self.msg.as_string()


class MailSender:
    def __init__(self, server, username, password):
        self.smtpserver = server
        self.username   = username
        self.password   = password

    def send(self, msg):
        try:
            conn = smtplib.SMTP(self.smtpserver)
            conn.set_debuglevel(1)
            conn.login(self.username, self.password)
            conn.sendmail(msg.mailfrom, msg.mailto, msg.tostring())
            conn.quit()
            return True
        except Exception, e:
            return False


def send_mail(subject, msg, toaddrs, attach=None):
    m = MailMessage(subject, 'from@sample.com', toaddrs, msg)
    if attach:
        filepath = '/home/test/script/你好.txt'
        m.append_file(filepath, 'text/plain')

    sender = MailSender('smtp.test.com', 'from@sample.com', 'passwd')
    sender.send(m)

if __name__ == '__main__':
    send_mail(subject='title', msg='content', toaddrs=['to@sample.com', '123456@qq.com'], attach=1)
