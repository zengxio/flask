#flask
pip3 install flask

socket服务端
  wsgi：Web服务网关接口
    - wsgiref
	- werkzeug
	
flask基本使用以及配置
from flask import Flask,render_template,session
from .sessions import MySessionInterface

app = Flask(__name__) #__name__ 是import_name 避免重复
"""
import_name,
static_url_path=None,       #静态文件前缀 默认是/static 如http://127.0.0.1:5000/static/123.png
static_folder='static',     #静态文件路径 
template_folder='templates',#模板路径
instance_path=None,         #指定配置文件路径，默认就是去root_path,当前路径中查找
instance_relative_config=False, #True 才可以生效上面指定的位置文件路径
root_path=None              #当前路径
"""

#配置
#方法一
    # app.config['DEBUG']=True
    # app.debug=True  #是上面的子级，只是 把常用的可以点出来直接配置
    #app.session_interface
    #app.config.update({})
#方法二
    #去一个py文件中导入配置
    #app.config.from_pyfile('settings.py') #默认就去root_path当前程序目录查找该文件
    #如 settings.py
    #DEBUG=True  #注意配置变量一定要是大写

    #app.config.from_envvar("hjkhdksa")  #环境变量的值为python文件名称。内部调用from_pyfile方法
    #如 test.py
    # import os
    # os.environ['hjkhdksa']='settings'

    #app.config.from_mapping({'DEBUG':True}) #字典格式

    # app.config.from_object('settings.TestingConfig') #导入配置文件类.推荐使用。切换正式环境和测试环境方便
    #如settings.py
    # class Config(object):
    #     DEBUG = False
    #     TESTING = False
    #     DATABASE_URI = 'sqlite://:memory:'
    #
    # class ProductionConfig(Config):
    #     DATABASE_URI = 'mysql://user@localhost/foo'
    #
    # class DevelopmentConfig(Config):
    #     DEBUG = True
    #
    # class TestingConfig(Config):
    #     TESTING = True
    # PS: 从sys.path中已经存在路径开始写

#路由方法1
@app.route('/')
def hello_world():
    # return 'Hello World!'
    return render_template('hello.html') #指定渲染模板文件

#默认url请求参数类型有
"""
DEFAULT_CONVERTERS = {
    'default':          UnicodeConverter,
    'string':           UnicodeConverter,
    'any':              AnyConverter,
    'path':             PathConverter,
    'int':              IntegerConverter,
    'float':            FloatConverter,
    'uuid':             UUIDConverter,
}
"""
# @app.route('/index/<int:nid>') # #接收url请求参数，默认不能写正则表达式，需要自定义扩展
# def hello_world(nid):
#     print(nid)
#     return 'Hello World!'

#路由方法2
# def hello_world():
#     from flask import url_for
#     url=url_for('xxx') #根据endpoint 配置的名字反向生成url。默认就是函数名hello_world
#     print(url)
#     return 'Hello World!'
#
# app.add_url_rule('/',view_func=hello_world,endpoint='xxx',methods=['GET','POST']) #methods配置允许接收请求方法

#注册自定义的session
app.secret_key="jdkslajfklsa"
app.session_interface=MySessionInterface()
session['username']='zxy' #使用session

if __name__ == '__main__':
    app.run()

	
#flask自定制正则路由匹配
from flask import Flask, views, url_for
from werkzeug.routing import BaseConverter

app = Flask(import_name=__name__)


class RegexConverter(BaseConverter):
    """
    自定义URL匹配正则表达式
    """
    def __init__(self, map, regex):
        super(RegexConverter, self).__init__(map)
        self.regex = regex

    def to_python(self, value):
        """
        路由匹配时，匹配成功后传递给视图函数中参数的值
        :param value:
        :return:
        """
        return int(value)

    def to_url(self, value):
        """
        使用url_for反向生成URL时，传递的参数经过该方法处理，返回的值用于生成URL中的参数
        :param value:
        :return:
        """
        val = super(RegexConverter, self).to_url(value)
        return val #这是接收到的url请求参数值

# 添加到flask中
app.url_map.converters['regex'] = RegexConverter

@app.route('/index/<regex("\d+"):nid>')
def index(nid):
    print(url_for('index', nid=nid))
    return 'Index'

if __name__ == '__main__':
    app.run()
	

#自定制路由 以及 CBV，自定义模板方法
from flask import Flask,views,render_template

app = Flask(__name__)
# app.config['SERVER_NAME']="oldboy.com:5000"
# #subdomain 设置二级域名访问
# @app.route('/index/',subdomain='admin') #http://admin.oldboy.com:5000/index/
# def index():
#     return 'Index'

#访问url直接跳转
# @app.route('/index/',redirect_to='/home/')
# def index():
#     return 'Index'
# @app.route('/home/')
# def home():
#     return "home"

#defaults设置默认传的url参数值
# @app.route('/index/',defaults={'nid':9})
# def index(nid):
#     print(nid)
#     return 'Index'

#增加装饰器的方法
def auth(func):
    def inner(*args, **kwargs):
        print('before')
        result = func(*args, **kwargs)
        print('after')
        return result
    return inner

# @app.route('/index.html', methods=['GET', 'POST'], endpoint='index')
# @auth  #先执行才有效
# def index():
#     return 'Index'

#CBV
#方法1

# class IndexView(views.View):
#     methods = ['GET']
#     decorators = [auth, ]  #增加装饰器的方法
#
#     def dispatch_request(self): #实现该方法调用不同的方法处理请求
#         print('Index')
#         return 'Index!'

# app.add_url_rule('/index', view_func=IndexView.as_view(name='index'))  # name=endpoint

#方法2

# class IndexView(views.MethodView):
#     methods = ['GET']
#     decorators = [auth, ]
#
#     def get(self):
#         return 'Index.GET'
#
#     def post(self):
#         return 'Index.POST'
#
#
# app.add_url_rule('/index', view_func=IndexView.as_view(name='index'))  # name=endpoint

# @app.route('/index',strict_slashes=False) #strict_slashes默认严格要求url末尾加/
# def index():
#     return "INDEX"

#自定义模板方法
def auth():
    return "<h1>auth</h1>"

@app.route('/index')
def index():
    return render_template('index.html',ww=auth)

"""
index.html
{{ww()|safe}}
"""


"""
请求处理方法
    from flask import Flask
    from flask import request  #直接导入就可以获取数据。flask默认封装一个环境变量赋值给request
    from flask import render_template
    from flask import redirect
    from flask import make_response

    app = Flask(__name__)


    @app.route('/login.html', methods=['GET', "POST"])
    def login():

        # 请求相关信息
        # request.method
        # request.args #get
        # request.form #post
        # request.values
        # request.cookies
        # request.headers
        # request.path
        # request.full_path
        # request.script_root
        # request.url
        # request.base_url
        # request.url_root
        # request.host_url
        # request.host
        # request.files
        # obj = request.files['the_file_name']
        #直接保存文件
        # obj.save('/var/www/uploads/' + secure_filename(f.filename))

        # 响应相关信息
        # return "字符串"
        # return render_template('html模板路径',**{})
        # return redirect('/index.html')
        
        #封装cookie信息在返回请求
        # response = make_response(render_template('index.html'))
        # response是flask.wrappers.Response类型
        # response.delete_cookie('key')
        # response.set_cookie('key', 'value')
        # response.headers['X-Something'] = 'A value' #设置请求头
        # return response


        return "内容"

    if __name__ == '__main__':
        app.run()
"""
if __name__ == '__main__':
    app.run()


	
flask session组件 pip3 install Flask-Session
session 默认放在加密cookie中
也可以自定制session
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
							
#注册自定义的session
app.secret_key="jdkslajfklsa"
app.session_interface=MySessionInterface()


蓝图:创建程序目录
如在flask目录下创建一个s4day127目录
run.py与s4day127目录同级
#!/usr/bin/env python
#encoding:utf-8

from s4day127 import app
if __name__ == '__main__':
    app.run()


s4day127目录下创建一个views的目录与__init__.py

__init__.py
#!/usr/bin/env python
#encoding:utf-8
from flask import Flask
app=Flask(__name__)
from .views.account import account
#注册成蓝图
app.register_blueprint(account)


views的目录下创建一个acccount.py
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


message 闪现
message是一个基于Session实现的用于保存数据的集合，其特点是：使用一次就删除。
#应用场景，错误提示，跳转页面传值
from flask import Flask, flash, redirect, render_template, request, get_flashed_messages
app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index1():
    messages = get_flashed_messages()
    print(messages)
    return "Index1"

@app.route('/set')
def index2():
    v = request.args.get('p')
    flash(v)
    return 'ok'

if __name__ == "__main__":
    app.run()

插件:
  Flask-Session
  WTForms
  SQLAchemy

flask自定制中间件
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/index')
def index1():
    return "Hello world"


class MiddleWare:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    #environ,start_response 连接sock的时候，wsgi自动传值到__call__方法
    #请求访问程序，先执行__call__方法
    def __call__(self, environ,start_response):
        print("before")
        response=self.wsgi_app( environ,start_response)
        #response 是经历过路由，处理请求后返回的结果
        print("after")
        return response


if __name__ == "__main__":
    #注册中间件
    app.wsgi_app = MiddleWare(app.wsgi_app)
    app.run(port=9999)
	


