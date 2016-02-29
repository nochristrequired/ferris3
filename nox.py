import os
from tempfile import gettempdir


def session_lint(session):
    session.install('flake8', 'flake8-import-order')
    session.run(
        'flake8',
        '--max-complexity=10',
        '--import-order-style=google',
        'ferris3', 'tests')


def session_tests(session):
    tmpdir = gettempdir()
    session.interpreter = 'python2.7'
    session.install(
        'git+https://github.com/GoogleCloudPlatform/python-repo-tools')
    session.install('-r', 'requirements-dev.txt')
    session.install('-e', '.')
    tests = session.posargs or ['tests/']
    session.run('gcprepotools', 'download-appengine-sdk', tmpdir)
    session.run(
        'nosetests', '--with-ferris', '--logging-level', 'INFO',
        '--gae-sdk-path', os.path.join(tmpdir, 'google_appengine'),
        '--with-coverage', '--cover-package', 'ferris3', '--cover-branches',
        '--cover-erase', *tests)
