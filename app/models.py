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
from hashlib import md5
from flask_login import UserMixin
from . import login_manager
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to guess'
# # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名jianshu,连接方式参考 \
# # http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/yqinfo'
# # 设置这一项是每次请求结束后都会自动提交数据库中的变动
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# # 实例化
# db = SQLAlchemy(app)


class User(UserMixin, db.Model):

    __tablename__ = 'user'
    user_id = db.Column(db.String(64), primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<{},{},{}>'.format(self.user_name, self.email, self.user_id)

    # 增加密码属性
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 设置密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 校验密码
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.user_id

    def generate_auth_token(self, expiration=3600):
        #生成令牌字符串token
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'user_id': self.user_id}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return None  # valid token, but expired
        return User.query.get(data['user_id'])


class Participator(db.Model):

    __tablename__ = 'participator'
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    wx = db.Column(db.String(20), nullable=False)
    PhoneNum = db.Column(db.String(11), nullable=False)
    IDNum = db.Column(db.String(18), nullable=False)
    Name = db.Column(db.String(30), nullable=False)
    NickName = db.Column(db.String(128), default='')
    Sex = db.Column(db.String(2), nullable=False)
    Birthday = db.Column(db.Date(), nullable=False)
    IncidenceTime = db.Column(db.String(10), nullable=False)
    IsDiagnosed = db.Column(db.String(2), nullable=True)
    DiagnosedTime = db.Column(db.Date(), nullable=True)
    IsArthritis = db.Column(db.String(2), nullable=True)
    ArthritisTime = db.Column(db.Date(), nullable=True)
    HashInput = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return "<name %s>" % self.Name


class Result(db.Model):

    __tablename_ = 'result'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    Height = db.Column(db.String(12), nullable=False)
    Weight = db.Column(db.String(12), nullable=False)
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
    PR1 = db.Column(db.String(32), nullable=True)
    PR2 = db.Column(db.String(32), nullable=True)
    PR3 = db.Column(db.String(32), nullable=True)
    PR4 = db.Column(db.String(32), nullable=True)
    PR5 = db.Column(db.String(32), nullable=True)
    PR6 = db.Column(db.String(32), nullable=True)
    PR7 = db.Column(db.String(32), nullable=True)
    propose = db.Column(db.Text(), nullable=True, default='')
    CreateTime = db.Column(db.DateTime(), default=datetime.now)
    HashInput = db.Column(db.String(32), nullable=False)
    message = db.Column(db.Text(), default='')

    def __repr__(self):
        return "<name %s>" % self.CreateTime


def hash_md5(val):
    return md5(val.encode('utf-8')).hexdigest()


# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    result = User.query.paginate(1, per_page=3, error_out=False)
    print(result.items)

