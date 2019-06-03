#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/16/19 11:22 PM
# @Author  : Lbsx
# @File    : email.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;
from flask import render_template
from flask_mail import Message
from . import mail
PREFIX= '[Flasky]'
SENDER= 'hexinpy@163.com'
def send_email(to, subject, template, **kwargs):
	msg = Message(PREFIX+subject, sender=SENDER, recipients=[to])
	msg.body = render_template(template+'.txt', **kwargs)
	msg.html = render_template(template+'.html', **kwargs)
	mail.send(msg)
