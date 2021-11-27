from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from admin_keys import admin_keys
from db import Users, Books

api = Blueprint('api', __name__, template_folder='templates')


def is_admin():
    if request.authorization is None:
        return False
    return request.authorization.username == 'admin' and request.authorization.password in admin_keys


def is_user():
    if request.authorization is None:
        return False
    user = Users.query.filter_by(email=request.authorization.username).first()
    return user is not None and check_password_hash(user.password, request.authorization.password)


@api.route('/book', methods=['GET'])
def book():
    if is_user() or is_admin():
        if request.args.get('name', None) is None:
            return jsonify(code='404', reason='Parameter "name" does not specified'), 404
        book = Books.query.filter_by(name=request.args['name']).first()
        if book is None:
            return jsonify(code='404', reason='The book with the specified name does not exist'), 404
        return jsonify(code='200', book=
        {
            'name': book.name,
            'author': book.author,
            'info': book.info,
            'count': book.count,
            'available_count': book.available_count,
            'reservations': [{
                'user_id': r.user.id,
                'expiry_date': str(r.expiry_date)[:10],
                'is_read': r.is_read
            } for r in book.reservations]
        })
    else:
        return jsonify(code='404', reason='You are not authorized with basic token'), 404


@api.route('/books', methods=['GET'])
def books():
    if is_user() or is_admin():
        books = Books.query.order_by(Books.id).limit(int(request.args['limit']) + 1) if request.args.get('limit',
                                                                                                         None) is not None else Books.query.all()
        return jsonify(books={book.name:
            {
                'name': book.name,
                'author': book.author,
                'info': book.info,
                'count': book.count,
                'available_count': book.available_count,
                'url': f'http://localhost:5000/api/book?name={book.name}',
                'reservations': [{
                    'username': r.user.name,
                    'expiry_date': str(r.expiry_date)[:10],
                    'is_read': r.is_read
                } for r in book.reservations]
            }

            for book in books}, code='200')
    else:
        return jsonify(code='404', reason='You are not authorized with basic token'), 404


@api.route('/me', methods=['GET'])
def me():
    if is_user():
        user = Users.query.filter_by(email=request.authorization.username).first()
        return jsonify(code='200', user={
            'name': user.name,
            'email': user.email,
            'age': user.age,
            'created_at': str(user.created_at)[:10],
            'verified': user.verified,
            'reservations': [{
                'book_name': r.book.name,
                'expiry_date': str(r.expiry_date)[:10],
                'is_read': r.is_read
            } for r in user.reservations]})
    else:
        return jsonify(code='404', reason='You are not authorized with basic token or you are admin'), 404


@api.route('/user', methods=['GET'])
def get_user():
    if is_admin():
        if request.args.get('name', None):
            user = Users.query.filter_by(name=request.args['name']).first()
        elif request.args.get('email', None):
            user = Users.query.filter_by(email=request.args['email']).first()
        else:
            return jsonify(code='404', reason='Parameter "name" or "email" must be specified'), 404
        if user is None and request.args.get('name', None):
            return jsonify(code='404', reason='User with specified name does not exists'), 404
        if user is None and request.args.get('email', None):
            return jsonify(code='404', reason='User with specified email does not exists'), 404
        return jsonify(code='200', user={
            'name': user.name,
            'email': user.email,
            'age': user.age,
            'created_at': str(user.created_at)[:10],
            'verified': user.verified,
            'reservations': [{
                'book_name': r.book.name,
                'expiry_date': str(r.expiry_date)[:10],
                'is_read': r.is_read
            } for r in user.reservations]})
    else:
        return jsonify(code='404', reason='You are not admin'), 404
