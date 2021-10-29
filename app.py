# Import flask and flask-extensions
from flask import Flask, render_template
# Import other libraries

# Import my files
from db import db, migrate, Users, Books, Reservations
# Create app and import config
app = Flask(__name__)
app.config.from_pyfile('config.py')
# Init extensions with app
db.init_app(app)
migrate.init_app(app, db)

# Index page


@app.route('/', methods=['GET'])
def index():
    # Return index page
    return render_template('index.html')


# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
