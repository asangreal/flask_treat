#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/17 下午6:00
# @Author  : Aries
# @Site    :
# @File    : models.py.py
# @Software: PyCharm Community Edition

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess'
# # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名jianshu,连接方式参考 \
# # http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/yqinfo'
# # 设置这一项是每次请求结束后都会自动提交数据库中的变动
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# # 实例化
# db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = 'user'
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    wx = db.Column(db.String(20), nullable=False)
    PhoneNum = db.Column(db.String(11), nullable=False)
    IDNum = db.Column(db.String(18), nullable=False, unique=True)
    Name = db.Column(db.String(30), nullable=False)
    NickName = db.Column(db.String(30), default='')
    Sex = db.Column(db.String(2), nullable=False)
    Birthday = db.Column(db.Date(), nullable=False)
    Height = db.Column(db.String(12), nullable=False)
    Weight = db.Column(db.String(12), nullable=False)
    IncidenceTime = db.Column(db.String(10), nullable=False)
    HashInput = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return "<name %s>" % self.Name


class Result(db.Model):

    __tablename_ = 'result'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    saPASI1 = db.Column(db.Integer(), nullable=False)
    saPASI2 = db.Column(db.Integer(), nullable=False)
    saPASI3 = db.Column(db.Integer(), nullable=False)
    saPASI4 = db.Column(db.Integer(), nullable=False)
    saPASI5 = db.Column(db.Integer(), nullable=False)
    QualityOfLife = db.Column(db.Integer(), nullable=False)
    Arthritis1 = db.Column(db.Integer(), nullable=False)
    Arthritis2 = db.Column(db.Integer(), nullable=False)
    Arthritis3 = db.Column(db.Integer(), nullable=False)
    Arthritis4 = db.Column(db.Integer(), nullable=False)
    Arthritis5 = db.Column(db.Integer(), nullable=False)
    Arthritis6 = db.Column(db.Integer(), nullable=False)
    PR1 = db.Column(db.Integer(), nullable=False)
    PR2 = db.Column(db.Integer(), nullable=False)
    PR3 = db.Column(db.Integer(), nullable=False)
    PR4 = db.Column(db.Integer(), nullable=False)
    PR5 = db.Column(db.Integer(), nullable=False)
    PR6 = db.Column(db.Integer(), nullable=False)
    PR7 = db.Column(db.Integer(), nullable=False)
    propose = db.Column(db.Text(), nullable=True, default='')
    CreateTime = db.Column(db.DateTime(), default=datetime.now)
    HashInput = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return "<name %s>" % self.CreateTime

def hash_md5(val):
    return md5(val.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # id = '330682198907123x'
    # name = '绵绵'
    # ir = hash_md5(name+id)
    # wx = User(wx='dadfa', PhoneNum='13575465942', IDNum=id, Name=name,
    #           NickName='活人', Sex='1', Birthday='2018-07-01', Height='170', Weight='50', IncidenceTime='2018-01-01',
    #           HashInput=ir)
    # db.session.add_all([wx]),
    # db.session.commit()
    #
    # result = Result(
    # saPASI1 = 1,
    # saPASI2 = 2,
    # saPASI3 = 1,
    # saPASI4 = 1,
    # saPASI5 = 1,
    # QualityOfLife = 1,
    # Arthritis1 = 1,
    # Arthritis2 = 1,
    # Arthritis3 = 1,
    # Arthritis4 = 1,
    # Arthritis5 = 1,
    # Arthritis6 = 1,
    # PR1 = 1,
    # PR2 = 1,
    # PR3 = 1,
    # PR4 = 1,
    # PR5 = 1,
    # PR6 = 1,
    # PR7 = 1,
    # propose = '',
    # HashInput=ir)
    # db.session.add_all([result]),
    # db.session.commit()
    # print(result.id)
    result = User.query.paginate(1, per_page=3, error_out=False)
    print(result.items)

