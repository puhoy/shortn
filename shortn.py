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

import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

@manager.command
def test(coverage=True):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@manager.command
def profile(coverage=False):
    """Run profiling tests. (output goes to 'profile_*.png')"""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('profiling')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

if __name__ == '__main__':
    manager.run()
