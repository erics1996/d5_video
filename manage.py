from app import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db

manager = Manager(app)
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # manager.run()
    app.run(port=5051, host='127.0.0.1')
