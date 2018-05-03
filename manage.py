import os

from thermos import create_app, db
from thermos.models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('THERMOS_ENV') or 'dev')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username='Heavyman', email='heavyman@example.com', password='awesome'))
    db.session.commit()
    print('Database initialized successfully')


@manager.command
def dropdb():
    if prompt_bool('Are you sure you want to drop the database? Data will be lost permanently'):
        db.drop_all()
        print('Database dropped successfully')


if __name__ == '__main__':
    manager.run()
