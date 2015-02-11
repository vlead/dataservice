import unittest
import os
import json 
import requests
from flask import Flask
import flask.ext.testing
from flask.ext.testing import TestCase
from src import api
from src.db import db
from src.app import create_app
from src import config
from src.db import Lab
from tests import test_data

class MyTest(TestCase):

    TESTING = True
    config =  {
      'SQLALCHEMY_DATABASE_URI': 'mysql+oursql://root:root@localhost/info'
    }

    def create_app(self):
        app = create_app(self.config)
        print app
        return app

    def setUp(self):
        print config
        db.create_all()
        self.load_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def load_test_data(self):
        self.test_data = dict()
        self.test_data = test_data.data
        print type(self.test_data)

    def insert_data(self, data):
         print type(data)
         new_lab = Lab(**data)
         new_lab.save()

    def test_get_all_labs(self):
        print "test get all labs()"
        self.insert_data(self.test_data)
        r = self.client.get('http://localhost:5000/institutes')
        print r

if __name__ == '__main__':
  unittest.main()

