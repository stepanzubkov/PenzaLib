from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from flask_login import login_required

from admin_keys import admin_keys
from db import Users, Books, db, Reservations
from forms import AddBookForm, AddReservationForm, AcceptReservationForm

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET'])
@login_required
def index():
    if session.get('is_admin', None) is None:
        return redirect(url_for('.login'))
    users = Users.query.order_by(Users.id.desc()).limit(10)
    return render_template('admin/index.html', users=users)


@admin.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    if session.get('is_admin', None) is not None:
        return redirect(url_for('.index'))
    if request.method == 'POST':
        if request.form['admin_key'] in admin_keys:
            session['is_admin'] = True
            return redirect(url_for('.index'))
        else:
            flash('Неправильный ключ')
    return render_template('admin/login.html')


@admin.route('/book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        try:
            book = Books(name=form.name.data, author=form.author.data, info=form.info.data, count=form.count.data,
                         available_count=form.count.data)

            db.session.add(book)
            db.session.commit()

            return redirect(url_for('book', name=form.name.data))
        except Exception as e:
            print(e)
            db.session.rollback()
    return render_template('admin/book.html', form=form)


@admin.route('/add-reservation', methods=['GET', 'POST'])
@login_required
def add_reservation():
    form = AddReservationForm()
    form.user.choices = [(i.id, i.name) for i in Users.query.all()]
    form.book.choices = [(i.id, i.name) for i in Books.query.all()]
    if form.validate_on_submit():
        try:
            reservation = Reservations(user_id=form.user.data, book_id=form.book.data)
            book = Books.query.get(form.book.data)
            book.available_count = book.available_count - 1

            db.session.add(reservation)
            db.session.commit()

            return redirect(url_for('.index'))
        except Exception as e:
            print(e)
            db.session.rollback()
    return render_template('admin/add-reservation.html', form=form)


@admin.route('/accept-reservation', methods=['GET', 'POST'])
@login_required
def accept_reservation():
    form = AcceptReservationForm()
    form.user.choices = [(i.id, i.name) for i in Users.query.all()]
    form.book.choices = [(i.id, i.name) for i in Books.query.all()]
    if form.validate_on_submit():
        try:
            reservation = Reservations.query.filter_by(user_id=form.user.data, book_id=form.book.data).first()
            if reservation is None:
                flash('Данный читатель не читал эту книгу')
                raise
            reservation.is_read = True
            book = Books.query.get(form.book.data)
            book.available_count = book.available_count + 1

            db.session.add(reservation)
            db.session.commit()

            return redirect(url_for('.index'))
        except Exception as e:
            print(e)
            db.session.rollback()
    return render_template('admin/accept-reservation.html', form=form)
