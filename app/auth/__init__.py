#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/17/19 4:03 PM
# @Author  : Lbsx
# @File    : __init__.py.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views