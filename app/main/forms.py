#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/16/19 11:22 PM
# @Author  : Lbsx
# @File    : forms.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, \
	SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, Required
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField()

class EditProfileForm(FlaskForm):
	"""
	资料编辑表单
	"""
	name = StringField('Real name', validators=[Length(0,64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
	username = StringField('Username', validators=[
		DataRequired(),
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
			   "Username must have only letters, numbers dots or underscores")
	])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and \
				User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

	def validate_username(self, field):
		if field.data != self.user.username and \
				User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
	body = PageDownField("what's on your mind?", validators=[Required()])
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	body = StringField('Enter your comment', validators=[DataRequired()])
	submit = SubmitField('Submit')

