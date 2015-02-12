# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
import json

# from src import api
from src.db import db
from src.app import create_app
from src.db import Lab, Institute, Discipline, Technology, Developer
from test_data import lab_data, instt_data, disc_data, tech_data, dev_data


class MyTest(TestCase):

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

    def test_get_all_labs(self):
        print "test_get_all_labs()"
        # insert dependent table data
        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        # insert the lab test data
        new_lab = Lab(**lab_data)
        new_lab.save()
        # make request
        r = self.client.get('/labs')
        # response is in string, load as a python dict
        resp = json.loads(r.data)
        # assert if length of retrieved labs is equal to inserted data
        self.assertEqual(len(resp), 1)
        # assert if name attr of test data is same as retrieved data
        self.assertEqual(lab_data['name'], resp[0]['name'])

    def test_get_specific_lab(self):
        print "test_get_specific_lab()"
        # insert dependent table data
        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        # insert the lab test data
        new_lab = Lab(**lab_data)
        new_lab.save()
        # make request
        r = self.client.get('/labs/1')
        # response is in string, load as a python dict
        resp = json.loads(r.data)
        # assert if specific lab is loaded
        self.assertEqual(lab_data['name'], resp['name'])
        # assert if lab not found is working
        r = self.client.get('/labs/999')
        self.assert_404(r)

    def test_get_all_institutes(self):
        print "test_get_all_institutes()"
        # insert the institute test data
        new_instt = Institute(**instt_data)
        new_instt.save()
        # make request
        r = self.client.get('/institutes')
         # response is in string, load as a python dict
        resp = json.loads(r.data)
        # assert if length of retrieved institutes is equal to inserted data
        self.assertEqual(len(resp), 1)
        # assert if name attr of test data is same as retrieved data
        self.assertEqual(instt_data['name'], resp[0]['name'])

    def test_get_all_technologoes(self):
        print "test_get_all_technologies()"
        # insert the technologies test data
        new_technology = Technology(**tech_data)
        new_technology.save()
        # make request
        r = self.client.get('/technologies')
        # response is in string, load as a python dict
        resp = json.loads(r.data)
        # assert if length of retrieved technologies is equal to inserted data
        self.assertEqual(len(resp), 1)
        # assert if name attr of test data is same as retrieved data
        self.assertEqual(tech_data['name'], resp[0]['name'])
 
    def test_get_all_disciplines(self):
        print "test_get_all_disciplines()"
        disc = Discipline(**disc_data)
        disc.save()
        r = self.client.get('/disciplines')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(disc_data['name'], resp[0]['name'])

    def test_get_all_developers(self):
        print "test_get_all_developers()"
        dev = Developer(**dev_data)
        dev.save()
        r = self.client.get('/developers')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(dev_data['name'], resp[0]['name'])

if __name__ == '__main__':
    unittest.main()
