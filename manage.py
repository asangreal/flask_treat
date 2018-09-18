#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/24 下午3:04
# @Author  : Aries
# @Site    : 
# @File    : manage.py.py
# @Software: PyCharm Community Edition
import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import app.models

raw = create_app('production')
manager = Manager(raw)
migrate = Migrate(raw, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
