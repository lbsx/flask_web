#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/18/19 3:42 PM
# @Author  : Lbsx
# @File    : fake.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;
"""
生成虚拟用户和博客文章
"""
from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post

def users(count=100):
	fake = Faker()
	i = 0
	while i < count:
		u = User(email=fake.email(),
				 username=fake.user_name(),
				 password='password',
				 confirmed=True,
				 name=fake.name(),
				 location=fake.city(),
				 about_me=fake.text(),
				 member_since=fake.past_date())
		db.session.add(u)
		try:
			db.session.commit()
			i += 1
		except IntegrityError:
			db.session.rollback()

def posts(count=100):
	fake = Faker()
	user_count = User.query.count()

	for i in range(count):
		u = User.query.offset(randint(0, user_count -1)).first()
		p = Post(body=fake.text(),
				 timestamp=fake.past_date(),
				 author=u)
		db.session.add(p)
	db.session.commit()