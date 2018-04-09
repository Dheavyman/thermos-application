from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from thermos import db


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(number):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(number)

    def __repr__(self):
        return f'<Bookmark "{self.description}": "{self.url}">'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    password_harsh = db.Column(db.String)

    @property
    def password(self):
        return AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_harsh = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_harsh, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return f'<User {self.username}'
