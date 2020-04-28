# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddCrimeForm(FlaskForm):
    crime_name = StringField('Заголовок', validators=[DataRequired()])
    crime_text = TextAreaField('Текст публикации', validators=[DataRequired()])
    photo = TextAreaField('Фотографии (укажите имя файла)', validators=[DataRequired()])
    submit = SubmitField('Отправить')
