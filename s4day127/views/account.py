#!/usr/bin/env python
#encoding:utf-8

# from .. import app

# @app.route('/login.html')
# def login():
#     return "Login"


#设置成蓝图
from flask import Blueprint
# account=Blueprint('account',__name__)
#url加前缀http://127.0.0.1:5000/xxx/login.html
#设置模板路径和静态文件目录
account=Blueprint('account',__name__,url_prefix='/xxx',template_folder='',static_folder='')

@account.route('/login.html')
def login():
    return "Login"