from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from thermos import db

tags = db.Table('bookmark_tag',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
                )


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags, lazy='joined',
                            backref=db.backref('bookmarks', lazy='dynamic'))

    @staticmethod
    def newest(number):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(number)

    @property
    def tags(self):
        return ','.join([tag.name for tag in self._tags])

    @tags.setter
    def tags(self, names):
        if names:
            self._tags = [Tag.get_or_create(name) for name in names.split(',')]

    def __repr__(self):
        return f'<Bookmark "{self.description}": "{self.url}">'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_harsh = db.Column(db.String, nullable=False)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

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


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    def __repr__(self):
        return f'{self.name}'
