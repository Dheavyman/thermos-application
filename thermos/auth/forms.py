from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, Email, ValidationError

from thermos.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')


class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(3, 80),
                                       Regexp('^[A-Za-z0-9_]{3,}$',
                                              message='Username consist of letters, numbers and underscore')])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    @staticmethod
    def validate_username(username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username already exist')

    @staticmethod
    def validate_email(email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('This email already exist')
