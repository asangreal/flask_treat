#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 下午5:52
# @Author  : Aries
# @Site    : 
# @File    : views.py
# @Software: PyCharm Community Edition
from . import www_site
from flask import jsonify, request, render_template


@www_site.route('/site')
def index():
    return 'this is www_site...'


@www_site.route('/user', methods=['GET'])
def users():
    return 'this users site'
