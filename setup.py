from setuptools import setup

requires = [
    'Flask',
    'Flask-SQLAlchemy',
    'oursql',
    'requests'
]

setup(
    name='DataService',
    version='0.1',
    install_requires=requires
)
