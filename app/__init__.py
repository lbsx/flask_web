#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 5/16/19 11:23 PM
# @Author  : Lbsx
# @File    : __init__.py
# @Software: PyCharm
# Copyright © 2019 Free Software Foundation,Inc.  
# License GPLv3+;

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from config import config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_pagedown import PageDown
from flask_session import Session

session = Session()

bootstrap = Bootstrap()
moment = Moment()
mail = Mail()

db = SQLAlchemy()
migrate = Migrate()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	bootstrap.init_app(app)
	moment.init_app(app)
	mail.init_app(app)
	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	pagedown.init_app(app)
	return app
