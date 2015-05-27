#!/usr/bin/env python
#coding=utf-8
import time
from datetime import datetime 
from datetime import timedelta

today = datetime.now()
aday = timedelta(days=1)
tommorow = today + aday
yestoday = today - aday
#last_month = time.localtime()[1]-1 or 12
last_month = time.localtime()[1]-1

print 'Today is:',today.strftime('%Y-%m-%d')
print 'Tommorow is:',tommorow.strftime('%Y-%m-%d')
print 'Yestoday is:',yestoday.strftime('%Y-%m-%d')
print 'Now is:',today.strftime('%H:%M:%S')
print 'Last month is:',last_month

