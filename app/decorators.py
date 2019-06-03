#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/17/19 11:19 PM
# @Author  : Lbsx
# @File    : decorators.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user.can(permission):
				abort(403)
			return f(*args, **kwargs)
		return decorated_function
	return decorator

def admin_required(f):
	return permission_required(Permission.ADMIN)(f)

