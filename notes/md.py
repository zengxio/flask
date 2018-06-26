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