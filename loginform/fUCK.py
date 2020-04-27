# -*- coding: utf-8 -*-
from flask import Flask, redirect, session, render_template
from flask_wtf import FlaskForm
from db import DB, UsersModel, NewsModel, RecepieModel
from loginform import LoginForm
from recepieform import AddRecepieForm
from addnewsform import AddNewsForm
from registrationform import RegistrationForm
import random
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db = DB()
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        session.pop('username', 0)
        session.pop('user_id', 0)
    except Exception:
        pass
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]

        return redirect("/index")
    return render_template('login.html', title='TattleCrime.com',
                           form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        session.pop('username', 0)
        session.pop('user_id', 0)
    except Exception:
        pass
    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        age = form.age.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if not (exists[0]):
            um = UsersModel(db.get_connection())
            um.insert(user_name, password, age)
            return redirect("/login")
    return render_template('registration.html', title='Tattle Crime',
                           form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    news = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('index.html', username=session['username'],
                           news=news)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        date = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
        breakfast = form.breakfast.data
        lunch = form.lunch.data
        dinner = form.dinner.data
        BKal = form.BKal.data
        LKal = form.LKal.data
        DKal = form.DKal.data
        kallories = BKal + LKal + DKal
        health = form.health.data
        weight = form.weight.data
        nm = NewsModel(db.get_connection())
        nm.insert(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")), breakfast,
                  session['user_id'], dinner, lunch,
                  BKal, DKal, LKal, health, weight)
        return redirect("/index")
    return render_template('add_news.html', title='Дневник питания',
                           form=form, username=session['username'])


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/info', methods=['GET', 'POST'])
def info():
    if 'username' not in session:
        return redirect('/login')
    return render_template('info.html', title='Дневник питания')


@app.route('/recepies', methods=['GET', 'POST'])
def recepies():
    if 'username' not in session:
        return redirect('/login')
    recepies = RecepieModel(db.get_connection()).get_all()
    return render_template('recepies.html', username=session['username'],
                           recepies=recepies)


@app.route('/add_recepie', methods=['GET', 'POST'])
def add_recepie():
    if 'username' not in session:
        return redirect('/login')
    form = AddRecepieForm()
    if form.validate_on_submit():
        recepie_name = form.recepie_name.data
        recepie_text = form.recepie_text.data
        recepie_kals = form.recepie_kals.data
        rm = RecepieModel(db.get_connection())
        rm.insert(recepie_name, recepie_text, recepie_kals,
                  session['username'])
        return redirect("/recepies")
    return render_template('add_recepie.html', title='Дневник питания',
                           form=form, username=session['username'])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
