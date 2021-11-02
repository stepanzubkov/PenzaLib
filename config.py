from re import S

from flask_mail import Mail


DEBUG = True
SECRET_KEY = 'fjgh748rsjgi847w890d84y97u9u9utg943-9trguu-039'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://stepan:123456@localhost:5432/plib'
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'Penza Library'
MAIL_DEFAULT_SENDER = 'fiveweek234@gmail.com'
MAIL_PASSWORD = 'Zubkov123456'
