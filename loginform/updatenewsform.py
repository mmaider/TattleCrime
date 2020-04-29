# -*- coding: utf-8 -*-
from flask import Flask, redirect, session, render_template
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired
import datetime


class UpdateNewsForm(FlaskForm):
    handle = open("godblessfaywray.txt", "r")
    data = handle.readlines()
    handle.close()
    date = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    pub_time = DateField('Дата ' + date)
    title = TextAreaField('Заголовок статьи', default=data[0], validators=[DataRequired()])
    news_text = TextAreaField('Текст публикации', default=data[1], validators=[DataRequired()])
    comments = TextAreaField('Ваши заметки', default=data[2], validators=[DataRequired()])
    status = SelectField('Статус работы', default=data[3], choices=[
        ("Заморожено", "Заморожено"),
        ("В процессе", "В процессе"),
        ("Последние правки", "Последние правки"),
        ("Готово к публикации", "Готово к публикации")])
    submit = SubmitField('Сохранить')