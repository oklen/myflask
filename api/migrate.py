from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app, db

migrate = Migrate(app, db)
manger = Manager(app)
manger.add_command('db', MigrateCommand)

if '__main__' == __name__:
    manger.run()
