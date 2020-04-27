from werkzeug.security import generate_password_hash

class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = AddNewsForm()
    return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'])

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')