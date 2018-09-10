import os
import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app

from app.textmp.models import TextMP
from app.imagemp.models import ImageMP
from app.user.models import User

app = create_app(config_name='development')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """runs unit tests wo test coverage"""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()