# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
# import json

from src.db import *
from src.app import create_app


class DBTest(TestCase):

    TESTING = True
    config = {
        'SQLALCHEMY_DATABASE_URI': ''
    }

    def create_app(self):
        app = create_app(self.config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_experiment(self):
        pass

    def test_set_developer_name(self):
        print "test_set_developer_name()"
        instt = Institute(name="MIT")
        dev = Developer(name="Joe", institute=instt, email_id="joe@example.com")
        new_name = Name("John")
        print "dev", new_name
        print new_name, type(new_name)
        dev.set_name(new_name)
        self.assertEqual(dev.name, "John")
        self.assertRaises(TypeError, dev.set_name, "John")

    def test_name_type(self):
        new_name = Name("John")
        self.assertEqual(new_name.value, "John")
        self.assertRaises(TypeError, Name, "123dasd")

    # Test for set_dnc attribute of Discipline entity
    def test_set_dnc(self):
        print "test_set_dnc()"
        disc = Discipline()
        new_dnc = Name("James")
        print new_dnc, type(new_dnc)
        disc.set_dnc(new_dnc)
        self.assertEqual(disc.dnc, "James")
        self.assertRaises(TypeError, disc.set_dnc, "James")

if __name__ == '__main__':
    unittest.main()
