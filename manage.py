from app import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db

app = create_app()
manager = Manager(app)
Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)
"""
数据库迁移命令：
python manage.py db init
python manage.py db migrate # 相当于Django中makemigrations
python manage.py db upgrade # 相当于Django中的migrate
"""
if __name__ == '__main__':
    manager.run()
    # app.run(port=5051)
