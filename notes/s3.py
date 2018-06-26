
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

