#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 下午5:51
# @Author  : Aries
# @Site    : 
# @File    : __init__.py
# @Software: PyCharm Community Edition

from flask import Blueprint

www_site = Blueprint(name='www_site', import_name=__name__)

from app.main_site import views
