#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/5 下午8:54
# @Author  : Aries
# @Site    : 
# @File    : caculate.py
# @Software: PyCharm Community Edition
from hashlib import md5
from app.models import User, Result
from app import db
from app.interface.advice import Advices


class CaculateRisk(object):

    risk_message1 = '建议就近就诊'
    risk_message2 = '建议外用治疗，并且持续观察'
    risk_message3 = '建议心理干预，可通过微信等移动网络方式'
    risk_message4 = '建议干预风险因素，精准患教'

    def __init__(self, request_json):
        self.request_json = request_json
        self.user = User()
        self.result = Result()
        self.advice = Advices()

    @property
    def wx_name(self):
        return self.request_json['WX']

    @property
    def phone_num(self):
        return self.request_json['PhoneNum']

    @property
    def id_num(self):
        return self.request_json['IDNum']

    @property
    def name(self):
        return self.request_json['Name']

    @property
    def nick_name(self):
        return self.request_json['NickName']

    @property
    def sex(self):
        if self.request_json['Sex'] == 0:
            sex = '女'
        elif self.request_json['Sex'] == 1:
            sex = '男'
        else:
            sex = ''
        return sex

    @property
    def birthday(self):
        return self.request_json['Birthday']

    @property
    def height(self):
        return self.request_json['Height']

    @property
    def weight(self):
        return self.request_json['Weight']

    @property
    def incidence_time(self):
        return self.request_json['IncidenceTime']

    @property
    def sapasi1(self):
        return int(self.request_json['saPASI1'])

    @property
    def sapasi2(self):
        return int(self.request_json['saPASI2'])

    @property
    def sapasi3(self):
        return int(self.request_json['saPASI3'])

    @property
    def sapasi4(self):
        return int(self.request_json['saPASI4'])

    @property
    def sapasi5(self):
        score = self.sapasi1 * (self.sapasi2 + self.sapasi3 + self.sapasi4)
        self.advice.qol_sapasi_message(self.quilityoflife, score)
        # if score > 9:
        #     self.message.append(self.risk_message1)
        # else:
        #     self.message.append(self.risk_message2)
        return score

    @property
    def quilityoflife(self):
        score = self.request_json['QualityOfLife']
        # if int(score) > 1:
        #     self.message.append(self.risk_message3)
        return score

    @property
    def arthritis1(self):
        return int(self.request_json['Arthritis1'])

    @property
    def arthritis2(self):
        return int(self.request_json['Arthritis2'])

    @property
    def arthritis3(self):
        return int(self.request_json['Arthritis3'])

    @property
    def arthritis4(self):
        return int(self.request_json['Arthritis4'])

    @property
    def arthritis5(self):
        return int(self.request_json['Arthritis5'])

    @property
    def arthritis6(self):
        score = self.arthritis1 + self.arthritis2 + self.arthritis3 + self.arthritis4 + self.arthritis5
        self.advice.pest_message(score)
        return score

    @property
    def risk1(self):
        if self.risk4 == '' or self.risk5 == '' or self.risk2 == '':
            return ''

        if self.request_json['PR1'] == '':
            return ''
        val = int(self.request_json['PR1'])
        if val > 3:
            return 0.22
        elif val < 3:
            return 1
        else:
            return 0.3

    @property
    def risk2(self):
        if self.request_json['PR2'] == '':
            return ''
        return int(self.request_json['PR2']) * 2.51

    @property
    def risk3(self):
        if self.risk4 == '' or self.risk5 == '' or self.risk2 == '':
            return ''

        if self.sapasi5 > 20:
            risk = 5.39
        elif self.sapasi5 < 10:
            risk = 1
        else:
            risk = 1.16
        return risk

    @property
    def risk4(self):
        if self.request_json['PR4'] == '':
            return ''
        return int(self.request_json['PR4']) * 3.42

    @property
    def risk5(self):
        if self.request_json['PR5'] == '':
            return ''
        return int(self.request_json['PR5']) * 31.5

    @property
    def risk6(self):
        if self.risk4 == '' or self.risk5 == '' or self.risk2 == '':
            return ''
        percent = float(self.weight) * 10000 / (float(self.height) * float(self.height))
        if percent > 27:
            # 肥胖
            return 2.03
        elif 23.0 < percent < 28:
            return 1.02
        else:
            return 0

    @property
    def risk7(self):
        if self.risk4 != '' and self.risk5 != '' and self.risk2 != '':
            risk = self.risk1 + self.risk2 + self.risk3 + self.risk4 + self.risk5 + self.risk6
            self.advice.pas_message(risk)
            return risk
        else:
            return ''

    def caculate(self):
        self.user_insert()
        message = list(set(self.advice.message))
        return self.sapasi5, self.arthritis6, self.risk7, ';'.join(message)

    def user_insert(self):
        user_md5 = hash_md5(self.name + self.id_num)
        res = self.check_user_is_in(user_md5)
        if not res:
            user_info = User(
                wx=self.wx_name,
                PhoneNum=self.phone_num,
                IDNum=self.id_num,
                Name=self.name,
                NickName=self.nick_name,
                Sex=self.sex,
                Birthday=self.birthday,
                Height=self.height,
                Weight=self.weight,
                IncidenceTime=self.incidence_time,
                HashInput=user_md5
            )
            db.session.add_all([user_info])
            db.session.commit()
        self.info_insert(user_md5)

    def info_insert(self, user_md5):
        result = Result(
            HashInput=user_md5,
            saPASI1=self.sapasi1,
            saPASI2=self.sapasi2,
            saPASI3=self.sapasi3,
            saPASI4=self.sapasi4,
            saPASI5=self.sapasi5,
            QualityOfLife=self.quilityoflife,
            Arthritis1=self.arthritis1,
            Arthritis2=self.arthritis2,
            Arthritis3=self.arthritis3,
            Arthritis4=self.arthritis4,
            Arthritis5=self.arthritis5,
            Arthritis6=self.arthritis6,
            PR1=self.risk1,
            PR2=self.risk2,
            PR3=self.risk3,
            PR4=self.risk4,
            PR5=self.risk5,
            PR6=self.risk6,
            PR7=self.risk7,
            propose=';'.join(list(set(self.advice.message)))
        )
        db.session.add_all([result])
        db.session.commit()

    def check_user_is_in(self, HashInput):
        return User.query.filter_by(HashInput=HashInput).all()


def hash_md5(val):
    return md5(val.encode('utf-8')).hexdigest()


def check_user_is_in(HashInput):
    return User.query.filter_by(HashInput=HashInput).all()


def result_page_getter_fiter(page, page_content_number, hash_input=None, result_query=True):
    pagination = Result.query.filter_by(HashInput=hash_input).order_by(Result.CreateTime.desc()).paginate(
        int(page), page_content_number, error_out=False)
    return pagination


def page_getter(page, page_content_number, hash_input=None, result_query=True):
    if result_query:
        pagination = Result.query.order_by(Result.CreateTime.desc()).paginate(
            int(page), page_content_number, error_out=False)
    else:
        pagination = User.query.paginate(page, page_content_number, error_out=False)
    return pagination


def recodes_getter(result_query=True):
    if result_query:
        num = Result.query.count()
    else:
        num = User.query.count()
    return num


def page_searcher(page, page_content_number, keyword, result_query=True):
    search_query = '%{0}%'.format(keyword)
    pagination = User.query(User.Name, User.IDNum).\
        filter_by(User.Name.like(search_query), User.IDNum.like(search_query)).\
        order_by(Result.CreateTime.desc()).paginate(
        int(page), page_content_number, error_out=False)
    print(pagination)
    if result_query:
        pagination = Result.query.filter_by()
