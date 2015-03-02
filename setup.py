from setuptools import setup

requires = [
    'flask',
    'Flask-SQLAlchemy',
    'oursql',
    'flask-cors',
    'flask-testing',
    'requests'
]

setup(
    name='DataService',
    version='0.1',
    install_requires=requires
)
