import os
from base64 import b64encode
from random import choice
from threading import Thread

from flask import Flask, render_template, flash, abort, redirect, url_for, request
from flask_login import login_required, login_user, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

from admin import admin
from api import api
from db import db, migrate, Users, Books, Reservations
from forms import BooksForm, RegistrationForm, LoginForm
from login import manager
from user import User

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')

mail = Mail(app)

manager.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

manager.login_view = 'login'
manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
manager.login_message_category = 'error'


def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipient, template, **kwargs):
    msg = Message(
        subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.email.data in [u.email for u in Users.query.all()]:
            flash('Такой аккаунт уже существует', category='error')
        else:
            try:
                user = Users(name=form.name.data, email=form.email.data,
                             password=generate_password_hash(form.password.data),
                             age=form.age.data, verified=False,
                             access_key=b64encode(os.urandom(50)).decode('utf-8').replace('/', ''))

                db.session.add(user)
                db.session.commit()
                send_mail(subject="Регистрация Penza Lib", recipient=form.email.data, template='mail.html',
                          name=form.name.data, key=Users.query.filter_by(email=form.email.data).first().access_key)
                flash(
                    'На вашу почту было отправлено письмо с подтверждением', category='success')
            except Exception as e:
                print(e)
                db.session.rollback()
    return render_template('registration.html', form=form)


@app.route('/accept/<key>', methods=['GET', 'POST'])
def accept(key):
    try:
        user = Users.query.filter_by(access_key=key).first()
        user.verified = True
        db.session.commit()
        userlogin = User().create(user)
        login_user(userlogin, remember=True)
        return redirect(url_for('profile'))
    except Exception as e:
        print(e)
        db.session.rollback()
        abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    user = Users.query.filter_by(email=form.email.data).first() if form.email.data in [
        u.email for u in Users.query.all()] else None
    if form.validate_on_submit():
        if user and check_password_hash(user.password, form.password.data):
            if user.verified == False:
                flash('Почта не подтверждена')
            else:
                userlogin = User().create(user)
                login_user(userlogin, remember=form.remember.data)
                return redirect(url_for('profile'))
        else:
            flash('Неправильные данные', category='error')
    return render_template('login.html', form=form)


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user = Users.query.get(current_user.get_id())
    return render_template('profile.html', user=user)


@app.route('/books', methods=['GET'])
@login_required
def books():
    form = BooksForm()
    user = Users.query.get(current_user.get_id())
    books = Books.query.filter(
        Books.name.like(request.args.get('name') if str(request.args.get(
            'name')) != '' and str(request.args.get(
            'name')) != 'None' else '%'),
        Books.author.like(request.args.get('author') if str(request.args.get(
            'author')) != '' and str(request.args.get(
            'author')) != 'None' else '%'),
    )
    match request.args.get('sorting'):
        case 'standart':
            pass
        case 'by_name':
            books = sorted(books, key=lambda u: u.name)
        case 'by_author':
            books = sorted(books, key=lambda u: u.author)
        case 'desc_count':
            books = sorted(
                books, key=lambda u: u.available_count)
        case 'count':
            books = sorted(
                books, key=lambda u: u.available_count, reverse=True)
        case _:
            pass
    return render_template('books.html', form=form, books=books, choice=choice)


@app.route('/book/<name>', methods=['GET'])
@login_required
def book(name):
    book = Books.query.filter_by(name=name).first()
    if book is None:
        abort(404)
    rsv = Reservations.query.filter_by(
        user_id=current_user.get_id(), book_id=book.id).first()
    return render_template('book.html', book=book, choice=choice, rsv=rsv)


# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
