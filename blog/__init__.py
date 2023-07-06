import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# app context
with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)

from blog import routes
