from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1> Siema! </h1>'


@app.route('/user/<name>')
def user(name):
    return f'<h1> Siema {name}!</h1>'
