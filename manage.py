from thermos import app, db
from thermos.models import User
from flask_script import Manager, prompt_bool

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username='Heavyman', email='heavyman@example.com'))
    db.session.commit()
    print('Database initialized successfully')


@manager.command
def dropdb():
    if prompt_bool('Are you sure you want to drop the database? Data will be lost permanently'):
        db.drop_all()
        print('Database dropped successfully')


if __name__ == '__main__':
    manager.run()