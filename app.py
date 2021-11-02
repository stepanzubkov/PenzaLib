# Import flask and flask-extensions
from flask import Flask, render_template, flash, abort
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
# Import other libraries
from base64 import b64encode
import os
from threading import Thread
# Import my files
from db import db, migrate, Users, Books, Reservations
from forms import RegistrationForm
# Create app and import config
app = Flask(__name__)
app.config.from_pyfile('config.py')
# Create mail instance
mail = Mail(app)
# Init extensions with app
db.init_app(app)
migrate.init_app(app, db)


def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipient, template, **kwargs):
    msg = Message(
        subject,      sender=app.config['MAIL_DEFAULT_SENDER'],  recipients=[recipient])
    msg.html = render_template(template,  **kwargs)
    thr = Thread(target=async_send_mail,  args=[app,  msg])
    thr.start()
    return thr

# Index page


@app.route('/', methods=['GET'])
def index():
    # Return index page
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.email.data in [u.email for u in Users.query.all()]:
            flash('Такой аккаунт уже существует', category='error')
        else:
            try:
                user = Users(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data),
                             age=form.age.data, verified=False, access_key=b64encode(os.urandom(50)).decode('utf-8').replace('/', ''))

                db.session.add(user)
                db.session.commit()

                send_mail(subject="Регистрация Penza Lib", recipient=form.email.data, template='mail.html',
                          name=form.name.data, key=Users.query.filter_by(email=form.email.data).first().access_key)
                flash('Вам отправлено письмо')
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
        return f'Успешная регистрация!'
    except Exception as e:
        print(e)
        db.session.rollback()
        abort(404)


# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
