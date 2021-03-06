import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# configure database
app.debug = False
app.config['SECRET_KEY'] = b'\xf6<FV\x9a\xd7\x8e\xf1\xa0\xdb\x97\x87:KP\xd0\xb2X\xcbH\xd2~Gc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
db = SQLAlchemy(app)

# configure authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to continue'
login_manager.init_app(app)

# Configure timestamps display
moment = Moment(app)

# Configure debugger
toolbar = DebugToolbarExtension(app)

from thermos import models, views
