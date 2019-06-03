#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/16/19 11:25 PM
# @Author  : Lbsx
# @File    : manage.py.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;
from app import create_app
import os
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

app.secret_key = "fjdsakljfdsalkjfl"

# app.run()   # 使用flask run可以不要这个。
