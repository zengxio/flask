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
