from flask import render_template, redirect, url_for, flash

from thermos import app, db
from thermos.forms import BookmarkForm
from thermos.models import User, Bookmark


# Fake user login
def logged_in_user():
    return User.query.filter_by(username='Heavyman').first()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bookmark = Bookmark(user=logged_in_user(), url=url, description=description)
        db.session.add(bookmark)
        db.session.commit()
        flash(f'Stored "{description}"')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    print('Error==============', error)
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    print('Error=============', error)
    return render_template('500.html'), 500
