#!/usr/bin/env python
#encoding:utf-8
from flask import Flask
app=Flask(__name__)
from .views.account import account
#注册成蓝图
app.register_blueprint(account)