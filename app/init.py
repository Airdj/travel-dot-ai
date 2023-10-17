from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import FLASK_SECRET_KEY, username, password


YOUR_SECRET_KEY = FLASK_SECRET_KEY
your_username = username
your_password = password

bootstrap = Bootstrap()
db = SQLAlchemy()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://' \
                                        f'{your_username}:{your_password}' \
                                        f'@/travel_dot_ai_db?host=/var/run/' \
                                        f'postgresql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

