import os
from app import create_app, db
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
from flask import current_app, url_for




app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)



def make_shell_context():
    return dict(app=app, current_app=current_app)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("debug", Server(use_debugger=True, use_reloader=True, host='0.0.0.0'))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """run unittests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
