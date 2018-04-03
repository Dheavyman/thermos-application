from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash

from forms import BookmarkForm


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xf6<FV\x9a\xd7\x8e\xf1\xa0\xdb\x97\x87:KP\xd0\xb2X\xcbH\xd2~Gc'


class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        return '{}. {}.'.format(self.firstname[0], self.lastname[0])


bookmarks = []


def store_bookmark(url, description):
    bookmarks.append(dict(
        url=url,
        description=description,
        user='The user',
        date=datetime.utcnow()
    ))


def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        flash('Stored "{}"'.format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
