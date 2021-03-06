#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/17 下午5:58
# @Author  : Aries
# @Site    : 
# @File    : __init__.py
# @Software: PyCharm Community Edition
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
# 会话保护等级
login_manager.session_protection = 'strong'
# 设置登录页面端点
login_manager.login_view = 'www_site.index'


def create_app(config_name='production'):
    # __name__ 决定应用根目录
    app = Flask(__name__)
    # 初始化app配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 扩展应用初始化
    db.init_app(app)
    login_manager.init_app(app)
    #初始化蓝本
    from .interface import interface as interface_blueprint
    app.register_blueprint(interface_blueprint)
    from .main_site import www_site as main_site_blueprint
    app.register_blueprint(main_site_blueprint)
    return app

application = create_app()
