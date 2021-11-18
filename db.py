from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime, timedelta


convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    verified = db.Column(db.Boolean, default=False)
    access_key = db.Column(db.String(100), nullable=False)
    reservations = db.relationship(
        'Reservations', backref='user', lazy='dynamic', uselist=True)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    info = db.Column(db.Text, nullable=False)
    count = db.Column(db.Integer, default=0)
    available_count = db.Column(db.Integer, default=0)
    reservations = db.relationship(
        'Reservations', backref='book', lazy='dynamic', uselist=True)


class Reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    expiry_date = db.Column(
        db.DateTime, default=datetime.utcnow() + timedelta(days=30))
    is_read = db.Column(db.Boolean, default=False)
