#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uuid
import json
from flask.sessions import SessionInterface
from flask.sessions import SessionMixin
from itsdangerous import Signer, BadSignature, want_bytes


class MySession(dict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        self.sid = sid
        self.initial = initial
        #相当于创建一个字典dict({'k1':'v1'})
        super(MySession, self).__init__(initial or ())

    #一旦调用session直接保存，具有时时性
    # def __setitem__(self, key, value):
    #     super(MySession, self).__setitem__(key, value)
    #
    # def __getitem__(self, item):
    #     return super(MySession, self).__getitem__(item)
    #
    # def __delitem__(self, key):
    #     super(MySession, self).__delitem__(key)


class MySessionInterface(SessionInterface):
    session_class = MySession
    container = {} #存session键值对

    def __init__(self):
        import redis  #可以连接redis，存入redis
        self.redis = redis.Redis()

    def _generate_sid(self):
        return str(uuid.uuid4())

    def _get_signer(self, app):
        #给session id设置签名认证
        if not app.secret_key:
            return None
        return Signer(app.secret_key, salt='flask-session',
                      key_derivation='hmac')

    def open_session(self, app, request):
        """
        程序刚启动时执行，需要返回一个session对象
        """
        #获取随机字符串
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            #没有随机字符串 就生成一个
            sid = self._generate_sid()
            return self.session_class(sid=sid)

        #进行签名认证
        signer = self._get_signer(app)
        try:
            sid_as_bytes = signer.unsign(sid)
            sid = sid_as_bytes.decode()
        except BadSignature:
            #报错就重新生成
            sid = self._generate_sid()
            return self.session_class(sid=sid)

        # session保存在redis中
        # val = self.redis.get(sid)
        # session保存在内存中
        #获取session键值对
        val = self.container.get(sid)

        if val is not None:
            try:
                data = json.loads(val)
                return self.session_class(data, sid=sid)
            except:
                return self.session_class(sid=sid)
        return self.session_class(sid=sid)

    def save_session(self, app, session, response):
        """
        程序结束前执行，可以保存session中所有的值
        如：
            保存到resit
            写入到用户cookie
        """
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)

        val = json.dumps(dict(session)) #从对象里面获取键值对

        # session保存在redis中
        # self.redis.setex(name=session.sid, value=val, time=app.permanent_session_lifetime)
        # session保存在内存中
        self.container.setdefault(session.sid, val)

        #对随机字符串进行签名
        session_id = self._get_signer(app).sign(want_bytes(session.sid))

        response.set_cookie(app.session_cookie_name, session_id,
                            expires=expires, httponly=httponly,
                            domain=domain, path=path, secure=secure)