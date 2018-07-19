#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/18 上午9:19
# @Author  : Aries
# @Site    : 
# @File    : __init__.py
# @Software: PyCharm Community Edition
from flask import Blueprint

interface = Blueprint(name='interface', import_name=__name__)

from app.interface import views
