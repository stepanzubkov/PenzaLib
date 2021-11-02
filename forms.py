from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, FileField, PasswordField, SelectField, RadioField, ValidationError
from wtforms.validators import DataRequired, Email, Length, NoneOf


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(
        'Пустое поле'), Length(min=0, max=50, message="Недопустимая длина")])
    email = StringField('Email', validators=[DataRequired('Пустое поле'), Length(
        min=0, max=100, message='Недопустимая длина'), Email('Неправильная запись')])
    password = PasswordField('Пароль', validators=[DataRequired(
        'Пустое поле'), Length(min=0, max=100, message='Недопустимая длина')])
    repeat_password = PasswordField('Повтор пароль', validators=[DataRequired(
        'Пустое поле'), Length(min=0, max=100, message='Недопустимая длина')])
    age = SelectField('Возраст', choices=[(i, i) for i in range(10, 101)])
    submit = SubmitField('Зарегестрироваться')
