# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
# import json

from src.db import *


class DBTest(TestCase):

    TESTING = True
    config = {
        'SQLALCHEMY_DATABASE_URI': ''
    }

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_experiment(self):
        pass


if __name__ == '__main__':
    unittest.main()
