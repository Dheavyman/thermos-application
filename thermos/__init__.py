import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xf6<FV\x9a\xd7\x8e\xf1\xa0\xdb\x97\x87:KP\xd0\xb2X\xcbH\xd2~Gc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
db = SQLAlchemy(app)

from thermos import models, views
