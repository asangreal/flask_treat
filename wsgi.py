#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/18 下午2:17
# @Author  : Aries
# @Site    : 
# @File    : wsgi.py.py
# @Software: PyCharm Community Edition
from app import create_app

application = app = create_app('default')
app.run()
