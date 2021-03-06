# -*- coding: utf-8 -*-
from flask import Flask, redirect, session, render_template
from flask_wtf import FlaskForm
from PyQt5.QtWidgets import QFileDialog, QApplication
from db import DB, UsersModel, NewsModel, CrimeModel
from loginform import LoginForm
from crimeform import AddCrimeForm
from addnewsform import AddNewsForm
from updatenewsform import UpdateNewsForm, Settings
from registrationform import RegistrationForm
from searchform import SearchForm
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

        return redirect("/crimes")
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
        title = form.title.data
        news_text = form.news_text.data
        comments = form.comments.data
        status = form.status.data
        nm = NewsModel(db.get_connection())
        nm.insert(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")), title, news_text, comments, status,
                  session['user_id'])
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


@app.route('/update_news/<int:news_id>', methods=['GET', 'POST'])
def update_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    pars = nm.get(news_id)[2:-1]
    saved_settings = Settings()
    saved_settings.title = pars[0]
    saved_settings.news_text = pars[1]
    saved_settings.comments = pars[2]
    saved_settings.status = pars[3]
    form = UpdateNewsForm(obj=saved_settings)
    if form.validate_on_submit():
        form.populate_obj(saved_settings)
        title = form.title.data
        news_text = form.news_text.data
        comments = form.comments.data
        status = form.status.data
        nm.update(news_id, str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")), title, news_text, comments,
                  status,
                  session['user_id'])
        return redirect("/index")
    return render_template('add_news.html', title='TattleCrime',
                           form=form, username=session['username'])


@app.route('/info', methods=['GET', 'POST'])
def info():
    if 'username' not in session:
        return redirect('/login')
    return render_template('info.html', title='Дневник питания')


@app.route('/crimes', methods=['GET', 'POST'])
def crimes():
    if 'username' not in session:
        return redirect('/login')
    crimes = CrimeModel(db.get_connection()).get_lasts()
    return render_template('crimes.html', username=session['username'],
                           crimes=crimes)


@app.route('/sort_newest', methods=['GET', 'POST'])
def sort_newest():
    if 'username' not in session:
        return redirect('/login')
    crimes = CrimeModel(db.get_connection()).sort_newest()
    form = SearchForm()
    if form.validate_on_submit():
        searchtext = form.searchtext.data
        crimes = CrimeModel(db.get_connection()).findcrime(searchtext)
    return render_template('archive.html', username=session['username'], form=form,
                           crimes=crimes)


@app.route('/sort_oldest', methods=['GET', 'POST'])
def sort_oldest():
    if 'username' not in session:
        return redirect('/login')
    crimes = CrimeModel(db.get_connection()).sort_oldest()
    form = SearchForm()
    if form.validate_on_submit():
        searchtext = form.searchtext.data
        crimes = CrimeModel(db.get_connection()).findcrime(searchtext)
    return render_template('archive.html', username=session['username'], form=form,
                           crimes=crimes)


@app.route('/sort_likes', methods=['GET', 'POST'])
def sort_likes():
    if 'username' not in session:
        return redirect('/login')
    crimes = CrimeModel(db.get_connection()).sort_likes()
    form = SearchForm()
    if form.validate_on_submit():
        searchtext = form.searchtext.data
        crimes = CrimeModel(db.get_connection()).findcrime(searchtext)
    return render_template('archive.html', username=session['username'], form=form,
                           crimes=crimes)


@app.route('/sort_likes_desc', methods=['GET', 'POST'])
def sort_likes_desc():
    if 'username' not in session:
        return redirect('/login')
    crimes = CrimeModel(db.get_connection()).sort_likes_desc()
    form = SearchForm()
    if form.validate_on_submit():
        searchtext = form.searchtext.data
        crimes = CrimeModel(db.get_connection()).findcrime(searchtext)
    return render_template('archive.html', username=session['username'], form=form,
                           crimes=crimes)


@app.route('/archive', methods=['GET', 'POST'])
def archive():
    if 'username' not in session:
        return redirect('/login')
    crimes = CrimeModel(db.get_connection()).get_all()
    form = SearchForm()
    if form.validate_on_submit():
        searchtext = form.searchtext.data
        crimes = CrimeModel(db.get_connection()).findcrime(searchtext)
    return render_template('archive.html', username=session['username'], form=form,
                           crimes=crimes)


@app.route('/like_act/<crime_id>', methods=['GET', 'POST'])
def like_act(crime_id):
    rm = CrimeModel(db.get_connection())
    rm.like(crime_id)
    return redirect("/crimes")


@app.route('/add_crime', methods=['GET', 'POST'])
def add_crime():
    if 'username' not in session:
        return redirect('/login')
    form = AddCrimeForm()
    if form.validate_on_submit():
        crime_name = form.crime_name.data
        crime_text = form.crime_text.data
        photo = form.photo.data
        crime_likes = 0
        rm = CrimeModel(db.get_connection())
        rm.insert(crime_name, crime_text, str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")), crime_likes, photo,
                  session['username'])
        return redirect("/crimes")
    return render_template('add_crime.html', title='Дневник питания',
                           form=form, username=session['username'])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
