from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length


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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Пустое поле'), Length(
        min=0, max=100, message='Недопустимая длина'), Email('Неправильная запись')])
    password = PasswordField('Пароль', validators=[DataRequired(
        'Пустое поле'), Length(min=0, max=100, message='Недопустимая длина')])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class BooksForm(FlaskForm):
    name = StringField('Название', validators=[Length(
        min=0, max=50, message='Недопустимая длина')])
    author = StringField('Автор', validators=[Length(
        min=0, max=50, message='Недопустимая длина')])
    sorting = SelectField('Сортировка', choices=[
        ('standart', 'По умолчанию'),
        ('by_name', 'По имени'),
        ('by_author', 'По автору'),
        ('count', 'По возрастанию количества'),
        ('desc_count', 'По убыванию количества')
    ])
    submit = SubmitField('Поиск')


class AddBookForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired('Пустое поле'), Length(min=0, max=100,
                                                                                   message='Неверная длина')])
    author = StringField('Автор', validators=[DataRequired('Пустое поле'), Length(min=0, max=100,
                                                                                  message='Неверная длина')])
    info = TextAreaField('Описание', validators=[DataRequired('Пустое поле')])
    count = SelectField('Количество', choices=[(i, i) for i in range(1, 101)])
    submit = SubmitField('Создать')


class AddReservationForm(FlaskForm):
    user = SelectField('Читатель', coerce=int)
    book = SelectField('Книга', coerce=int)
    submit = SubmitField('Добавить')


class AcceptReservationForm(FlaskForm):
    user = SelectField('Читатель', coerce=int)
    book = SelectField('Книга', coerce=int)
    submit = SubmitField('Принять')
