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