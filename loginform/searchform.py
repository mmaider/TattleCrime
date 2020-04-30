from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searchtext = TextAreaField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Поиск')
