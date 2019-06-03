#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/16/19 11:22 PM
# @Author  : Lbsx
# @File    : __init__.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;
from flask import Blueprint

main = Blueprint('main', __name__)
from . import views
from ..models import Permission

@main.app_context_processor
def inject_permissions():
	return dict(Permission=Permission)
