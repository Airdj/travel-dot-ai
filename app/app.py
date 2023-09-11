from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import FLASK_SECRET_KEY, username, password


YOUR_SECRET_KEY = FLASK_SECRET_KEY
your_username = username
your_password = password

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://' \
                                        f'{your_username}:{your_password}' \
                                        f'@/travel_dot_ai_db?host=/var/run/' \
                                        f'postgresql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

from flask_db_management import final_prompter_by_loc_flask
# sorry :( temporary solution


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CityForm()
    if form.validate_on_submit():
        func_result = final_prompter_by_loc_flask(form.city.data)
        return render_template('index.html', form=form,
                               tables=[func_result.to_html(classes='data',
                                       index=False)],
                               titles=func_result.columns.values)
    else:
        return render_template('index.html', form=form)


@app.route('/user/<name>')
def user(name):
    return f'<h1> Siema {name}!</h1>'


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error():
    return render_template('500.html'), 500


class CityForm(FlaskForm):
    city = StringField('What city you would like to explore?', validators=[
        DataRequired()])
    submit = SubmitField('Try!')


if __name__ == '__main__':
    app.run()
