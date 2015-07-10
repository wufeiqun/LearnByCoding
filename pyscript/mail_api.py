#!/usr/bin/env python
#coding=utf-8
import os
from flask import Flask,request

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello,Rocky!!!'

@app.route('/mail',methods=['POST'])
#def send_mail(subject=request.form['sub'],content=request.form['con'],receiver=request.form['rec']):
def send_mail():
	#return 'Your request method is '+request.method+' and your request content is '+request.form['test']
	mail_cmd = 'echo '+request.form['con']+'|mail -s '+request.form['sub']+' '+request.form['rec']
	result = os.system(mail_cmd)
	if result == 0:
		return 'Sending mail successfully!'
	else:
		return 'Sending mail failed!'

if __name__ == '__main__':
	app.run(host='0.0.0.0')
