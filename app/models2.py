#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/16/19 6:38 PM
# @Author  : Lbsx
# @File    : models.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.ext import declarative
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, \
	Boolean
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import login_manager

Base = declarative.declarative_base()
engine = create_engine(
		"mysql+pymysql://leib:123@localhost:3306/miguel?charset=utf8",
		max_overflow=0,
		pool_size=5,
		pool_timeout=30,
		pool_recycle=-1 # 多久后对线程池中的线程进行一次连接回收（重置）
	)

class Permission:
	FOLLOW = 1
	COMMENT = 2
	WRITE = 4
	MODERATE = 8
	ADMIN = 16

def init_db():
	Base.metadata.create_all(engine)

class Role(Base):
	__tablename__ = "roles"
	id = Column(Integer, primary_key=True)
	name = Column(String(64), unique=True)
	default = Column(Boolean, default=False, index=True)
	permissions = Column(Integer)

	def __repr__(self):
		return '<Role %r>' % self.name

	# 关系
	#users = relationship('User', backref='role')
	# 动态关系
	users = relationship('User', backref='role', lazy='dynamic')

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if self.permissions is None:
			self.permissions = 0

	def add_permission(self, perm):
		if not self.has_permission(perm):
			self.permissions += perm

	def remove_permission(self, perm):
		if self.has_permission(perm):
			self.permissions -= perm

	def reset_permissions(self):
		self.permissions = 0

	def has_permission(self, perm):
		return self.permissions & perm == perm

	@staticmethod
	def insert_roles():
		roles = {
			'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
			'Moderator': [Permission.FOLLOW, Permission.COMMENT,
						  Permission.WRITE, Permission.MODERATE],
			'Administrator': [Permission.FOLLOW, Permission.COMMENT,
							  Permission.WRITE, Permission.MODERATE,
							  Permission.ADMIN],
		}
		default_role = 'User'
		for r in roles:
			role = session.query(Role).filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.reset_permissions()
			for perm in roles[r]:
				role.add_permission(perm)
			role.default = (role.name == default_role)
			session.add(role)
		session.commit()

class User(UserMixin, Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(64), unique=True, index=True)
	email = Column(String(64), unique=True, index=True)
	password_hash = Column(String(128))

	role_id = Column(Integer, ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

	@property
	def password(self):
		raise AttributeError("password is not a readable attribute")

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id}).decode('utf-8')

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		session.add(self)
		return True

def operate_db():
	# 清空数据库
	Base.metadata.drop_all(engine)

	# 创建表
	init_db()
	# 添加数据
	Session = sessionmaker(engine)
	session = Session()
	# 插入行
	admin_role = Role(name="Admin")
	mod_role = Role(name="Moderator")
	user_role = Role(name="User")
	user_john = User(username="john", role=admin_role)
	user_susan = User(username='susan', role=user_role)
	user_david = User(username='david', role=user_role)
	# session.add(admin_role)
	print(admin_role.id)  # None, 未写入数据库，所以没有值
	session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])
	session.commit()
	print(admin_role.id)  # 1

	# 修改行
	admin_role.name = "Administrator"
	session.add(admin_role)
	session.commit()

	# 删除行
	session.delete(mod_role)
	session.commit()

	# 查询行
	roles = session.query(Role).all()
	users = session.query(User).all()
	print(roles, '\n', users)
	session.query(User).filter_by(username='john')

	# 加lazy='dynamic'可以禁止自动执行查询
	print(user_role.users.order_by(User.username).all())


Session = sessionmaker(engine)
session = Session()

@login_manager.user_loader
def load_user(user_id):
	return session.query(User).get(int(user_id))
