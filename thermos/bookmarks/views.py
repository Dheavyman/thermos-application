from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from . import bookmarks
from .forms import BookmarkForm
from .. import db
from ..models import User, Bookmark, Tag


@bookmarks.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        tags = form.tags.data
        bookmark = Bookmark(user=current_user, url=url, description=description, tags=tags)
        db.session.add(bookmark)
        db.session.commit()
        flash(f'Stored "{description}"')
        return redirect(url_for('main.index'))
    return render_template('bookmark_form.html', form=form, title='Add a new bookmark')


@bookmarks.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash(f'Stored "{bookmark.description}"')
        return redirect(url_for('.user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title='Edit bookmark')


@bookmarks.route('/delete/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def delete(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(bookmark)
        db.session.commit()
        flash(f'Deleted {bookmark.description}')
        return redirect(url_for('.user', username=current_user.username))
    else:
        flash('Please confirm deleting bookmark.')
    return render_template('confirm_delete.html', bookmark=bookmark, nolinks=True)


@bookmarks.route('/users/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, new_bookmarks=user.bookmarks)


@bookmarks.route('/tags/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)
