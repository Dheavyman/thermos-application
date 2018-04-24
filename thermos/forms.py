from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Length, EqualTo, Regexp, Email, ValidationError

from thermos.models import User


class BookmarkForm(FlaskForm):
    url = URLField('Enter the URL:', validators=[DataRequired(), url()])
    description = StringField('Enter an optional description:')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                                                  message='Tags can only contains letters and numbers')])

    def validate(self):
        if not self.url.data.startswith('http://') or \
                self.url.data.startswith('https://'):
            self.url.data = 'http://' + self.url.data

        if not FlaskForm.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tag_set = set(not_empty)
        self.tags.data = ','.join(tag_set)

        return True


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

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username already exist')

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('This email already exist')
