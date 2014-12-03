from setuptools import setup

requires = [
    'tornado',
    'mongoengine'
]

setup(
    name='DataService',
    version='0.1',
    install_requires=requires
)
