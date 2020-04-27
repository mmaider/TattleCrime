# -*- coding: utf-8 -*-
from flask import Flask, redirect, session, render_template
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired
import datetime


class AddNewsForm(FlaskForm):
    date = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    title = DateField('Дата ' + date)
    breakfast = TextAreaField('Ваш завтрак', validators=[DataRequired()])
    lunch = TextAreaField('Ваш обед', validators=[DataRequired()])
    dinner = TextAreaField('Ваш ужин', validators=[DataRequired()])
    BKal = IntegerField('Калории за завтрак', validators=[DataRequired()])
    LKal = IntegerField('Калории за обед', validators=[DataRequired()])
    DKal = IntegerField('Калории за ужин', validators=[DataRequired()])
    health = SelectField('Оцените ваше самочувствие', choices=[
        ("плохо :(", "плохо :("),
        ("чувствую слабость", "чувствую слабость"),
        ("бодрость", "бодрость"),
        ("Полон/полна сил!", "Полон/полна сил!")])
    weight = IntegerField('Вес', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = AddNewsForm()
    return render_template('add_news.html', title='Дневник питания',
                           form=form, username=session['username'])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
