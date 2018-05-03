from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Regexp


class BookmarkForm(FlaskForm):
    url = URLField('Enter the URL:', validators=[DataRequired(), url()])
    description = StringField('Enter an optional description:')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                                                  message='Tags can only contains letters and numbers')])

    def validate(self):
        if not (self.url.data.startswith('http://') or
                self.url.data.startswith('https://')):
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
