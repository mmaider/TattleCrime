# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired


class AddRecepieForm(FlaskForm):
    recepie_name = StringField('Название блюда', validators=[DataRequired()])
    recepie_text = TextAreaField('Описание рецепта', validators=[DataRequired()])
    recepie_kals = FloatField('Калории в 100 г.', validators=[DataRequired()])
    submit = SubmitField('Отправить')
