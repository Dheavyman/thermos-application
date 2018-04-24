from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from thermos import app, db, login_manager
from thermos.forms import BookmarkForm, LoginForm, SignupForm
from thermos.models import User, Bookmark, Tag


# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template('bookmark_form.html', form=form, title='Add a new bookmark')


@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title='Edit bookmark')


@app.route('/delete/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def delete(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(bookmark)
        db.session.commit()
        flash(f'Deleted {bookmark.description}')
        return redirect(url_for('user', username=current_user.username))
    else:
        flash('Please confirm deleting bookmark.')
    return render_template('confirm_delete.html', bookmark=bookmark, nolinks=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(f'Logged in successfully as {user.username}.')
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {user.username}!, Please login to continue')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/users/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, new_bookmarks=user.bookmarks)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/tags/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)


@app.errorhandler(404)
def page_not_found(error):
    print('Error==============', error)
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    print('Error=============', error)
    return render_template('500.html'), 500


@app.context_processor
def inject_tags():
    return dict(all_tags=Tag.query.all)
