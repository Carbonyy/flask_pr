from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class ReviewForm(FlaskForm):
    movie_title = StringField('Название фильма', validators=[DataRequired()])
    rating = FloatField('Рейтинг (0-10)', validators=[DataRequired()])
    review_text = TextAreaField('Ваш отзыв', validators=[DataRequired()])
    image_url = StringField('URL изображения', validators=[DataRequired()])
    submit = SubmitField('Создать отзыв')
