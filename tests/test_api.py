# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
import json


# from src import api
from src.db import db
from src.app import create_app
from src.db import Lab, Institute, Discipline, Technology, Developer, Experiment, LabSystemInfo
from test_data import lab_data, instt_data, disc_data, tech_data, develop_data, exp_data, update_instt, update_disc, update_develop, update_tech, update_lab, sys_data, update_sys_data


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

    def test_put_specific_lab(self):
        print "test_put_specific_lab()"
        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        lab = Lab(**lab_data)
        lab.save()
        r = self.client.put('/labs/1', data=update_lab)
        resp = json.loads(r.data)
        self.assertNotEqual(lab_data['name'], resp['name'])


    def test_put_specific_inst(self):
        print "test_put_specific_inst()"
        instt = Institute(**instt_data)
        instt.save()
        r = self.client.put('/institutes/1',data=update_instt)
        resp = json.loads(r.data)
        self.assertNotEqual(instt_data['name'],resp['name'])

    def test_put_specific_disc(self):
        print "test_put_specific_disc()"
        disc = Discipline(**disc_data)
        disc.save()
        r = self.client.put('/disciplines/1',data=update_disc)
        resp = json.loads(r.data)
        self.assertNotEqual(disc_data['name'],resp['name'])

    def test_put_specific_develop(self):
        print "test_put_specific_disc()"
        develop = Developer(**develop_data)
        develop.save()
        r = self.client.put('/developers/1',data=update_develop)
        resp = json.loads(r.data)
        self.assertNotEqual(develop_data['name'],resp['name'])

    def test_put_specific_tech(self):
        print "test_put_specific_tech()"
        tech = Technology(**tech_data)
        tech.save()
        r = self.client.put('/technologies/1',data=update_tech)
        resp = json.loads(r.data)
        self.assertNotEqual(tech_data['name'],resp['name'])


    def test_post_specific_develop(self):
        print "test_post_specific_develop()"
        develop = Developer(**develop_data)
        develop.save()
        r = self.client.post('/developers',data=develop_data)
        #if r.status_code is 500:
        #    print ""
        resp = json.loads(r.data)
        self.assertEqual(develop_data['name'],resp['name'])

    def test_post_specific_instt(self):
        print "test_post_specific_instt()"
        instt = Institute(**instt_data)
        instt.save()
        r = self.client.post('/institutes',data=instt_data)
        resp = json.loads(r.data)
        self.assertEqual(instt_data['name'],resp['name'])

    def test_post_specific_disc(self):
        print "test_post_specific_disc()"
        disc = Discipline(**disc_data)
        disc.save()
        r = self.client.post('/disciplines',data=disc_data)
        resp = json.loads(r.data)
        self.assertEqual(disc_data['name'],resp['name'])

    def test_post_specific_tech(self):
        print "test_post_specific_develop()"
        tech = Technology(**tech_data)
        tech.save()
        r = self.client.post('/technologies',data=tech_data)
        resp = json.loads(r.data)
        self.assertEqual(tech_data['name'],resp['name'])

    def test_post_specific_lab(self):
        print "test_post_specific_lab()"
        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        lab = Lab(**lab_data)
        lab.save()
        r = self.client.post('/labs',data=lab_data)
        resp = json.loads(r.data)
        self.assertEqual(lab_data['name'],resp['name'])

    def test_post_specific_exp(self):
        print "test_post_specific_exp()"

        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        new_lab = Lab(**lab_data)
        new_lab.save()

        exp = Experiment(**exp_data)
        exp.save()
        r = self.client.post('/experiments',data=exp_data)
        resp = json.loads(r.data)
        self.assertEqual(exp_data['name'],resp['name'])



    def test_get_all_institutes(self):
        print "test_get_all_institutes()"
        new_instt = Institute(**instt_data)
        new_instt.save()
        r = self.client.get('/institutes')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(instt_data['name'], resp[0]['name'])

    def test_get_all_technologoes(self):
        print "test_get_all_technologies()"
        new_technology = Technology(**tech_data)
        new_technology.save()
        r = self.client.get('/technologies')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
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
        dev = Developer(**develop_data)
        dev.save()
        r = self.client.get('/developers')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(develop_data['name'], resp[0]['name'])

    def test_get_lab_by_institute(self):
        print "test_get_lab_by_institute()"
        # insert dependent table data
        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        # insert lab test data
        new_lab = Lab(**lab_data)
        new_lab.save()
        # make request
        r = self.client.get('/labs/institutes/1')
        resp = json.loads(r.data)
       # print resp
        self.assertEqual(len(resp), 1)
        self.assertEqual(instt_data['name'], resp[0]['institute']['name'])

    def test_all_labs_specific_discipline_specific_institute(self):
        print "test_all_labs_specific_discipline_specific_institute()"
        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        new_lab = Lab(**lab_data)
        new_lab.save()
        r = self.client.get('/labs/institutes/1/disciplines/1')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(lab_data['name'], resp[0]['name'])

    def test_get_lab_by_discipline(self):
        print "test_get_lab_by_discipline()"
        disc = Discipline(**disc_data)
        disc.save()
        inst = Institute(**instt_data)
        inst.save()
        new_lab = Lab(**lab_data)
        new_lab.save()
        r = self.client.get('/labs/disciplines/1')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(disc_data['name'], resp[0]['discipline']['name'])
        r = self.client.get('/labs/disciplines/999')
        self.assert_404(r)


    def test_get_experiments_of_a_lab(self):
	print "test_get_experiments_of_a_lab()"
	disc = Discipline(**disc_data)
        disc.save()
        inst = Institute(**instt_data)
        inst.save()
        new_lab = Lab(**lab_data)
        new_lab.save()
        exps = Experiment(**exp_data)
        exps.save()
        r = self.client.get('/labs/1/experiments')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(exp_data['name'], resp[0]['name'])
        r = self.client.get('/labs/999/experiments')
        self.assert_404(r)

    def test_get_search(self):
        print "test_get_search()"
        disc = Discipline(**disc_data)
        disc.save()
        inst = Institute(**instt_data)
        inst.save()
        new_lab = Lab(**lab_data)
        new_lab.save()
        r = self.client.get('/search/labs?status=Hosted')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(lab_data['status'], resp[0]['status'])

    def test_get_search_by_attr(self):
 	print "test_get_search_by_attr()"
        disc = Discipline(**disc_data)
        disc.save()
        inst = Institute(**instt_data)
        inst.save()
        new_lab = Lab(**lab_data)
        new_lab.save()
	r = self.client.get('/labs/1?fields=status')
	resp = json.loads(r.data)
	self.assertEqual(len(resp), 1)
	self.assertEqual(lab_data['status'], resp['status'])

    def test_get_labsysteminfo(self):
	print "test_get_labsysteminfo()"
	disc = Discipline(**disc_data)
        disc.save()
        inst = Institute(**instt_data)
        inst.save()
        new_lab = Lab(**lab_data)
        new_lab.save()
        new_system_info = LabSystemInfo(**sys_data)
        new_system_info.save()
        r = self.client.get('/labsysteminfo')
        resp = json.loads(r.data)
        self.assertEqual(len(resp), 1)
        self.assertEqual(sys_data['os'], resp[0]['os'])
      

    def test_post_labsysteminfo(self):
        print "test_post_labsysteminfo()"

        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        new_lab = Lab(**lab_data)
        new_lab.save()

        new_system_info = LabSystemInfo(**sys_data)
        new_system_info.save()
        r = self.client.post('/labsysteminfo',data=sys_data)
        resp = json.loads(r.data)
        self.assertEqual(sys_data['os'],resp['os'])

    def test_put_labsysteminfo(self):
        print "test_put_specific_lab()"
        instt = Institute(**instt_data)
        instt.save()
        disc = Discipline(**disc_data)
        disc.save()
        lab = Lab(**lab_data)
        lab.save()
        new_system_info = LabSystemInfo(**sys_data)
        new_system_info.save()
        
        r = self.client.put('/labsysteminfo/1', data=update_sys_data)
        resp = json.loads(r.data)
        self.assertNotEqual(sys_data['os'], resp['os'])





if __name__ == '__main__':
    unittest.main()
