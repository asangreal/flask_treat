#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/18 上午9:19
# @Author  : Aries
# @Site    :
# @File    : views.py
# @Software: PyCharm Community Edition
from app.interface import interface
import traceback
import time
import json
from app.models import User, Result
from flask import jsonify, request
from app.interface.caculate import CaculateRisk, hash_md5, result_page_getter_fiter, result_set


@interface.route('/Alldata', methods=['POST'])
def alldata():
    Result = 1
    content = {}
    json_return = {}
    try:
        cr = CaculateRisk(request.json)
        sapsi5, arthritis6, pr7, message, nid = cr.caculate()
        content = {'saPASI5': int(sapsi5), 'Arthritis6': int(arthritis6), 'PR7': round(pr7, 2) if pr7 else None,
                   'propose': message, 'ID': nid}
    except Exception as e:
        traceback.print_exc(file=open('error.txt', 'a'))
        Result = 2
    if content:
        json_return = content
    json_return['Result'] = Result
    return jsonify(json_return)


@interface.route('/getHistoryRecord', methods=['POST'])
def get_history():
    try:
        content = request.json
        ID_num = content['IDNum']
        name = content['Name']
        page = int(content['Page'])
        hash_input = hash_md5(name+ID_num)
        pagination = result_page_getter_fiter(page, page_content_number=8, hash_input=hash_input)
        page_val = []
        for page_content in pagination.items:
            page_val.append({
                'saPASI5': page_content.saPASI5,
                'Arthritis6': page_content.Arthritis6,
                'PR7': page_content.PR7,
                'propose': page_content.propose,
                # 'time ': time.strftime('%Y-%m-%d %H:%M:%S', page_content.CreateTime)
                'time': page_content.CreateTime.strftime('%Y-%m-%d %H:%M:%S')
            })
        json_return = {'result': 1, 'value': page_val}
    except Exception as e:
        traceback.print_exc(file=open('error.txt', 'a'))
        json_return = {'result': 2}
    return jsonify(json_return)


@interface.route('/sdk/err')
def err_test():
    err = {"error": "invaild_redirect"}
    return jsonify(err)


@interface.route('/sendMessage', methods=['POST'])
def upload_message():
    result = 1
    try:
        content = request.json
        ID_num = content['ID']
        message = content['message']
        result_set(message, ID_num)
    except Exception as e:
        result = 2
        traceback.print_exc(file=open('error.txt', 'a'))
    return jsonify({'result': result})
