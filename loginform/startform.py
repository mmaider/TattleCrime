# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired


class StartForm(FlaskForm):
    radiobuttons = RadioField('Label', choices=[('value', 'description'), ('value_two', 'whatever')])
    submit = SubmitField('Отправить!')
