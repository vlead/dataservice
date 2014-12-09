import unittest
import requests
#import subprocess
import json
import os
import threading

from mongoengine import connect
import tornado.web
import tornado.ioloop

from src.db import Lab
from src import api

TEST_DB_NAME = 'test-labs-info'


class TestAPI(unittest.TestCase):
    # helper functions

    # import tornado ioloop, our app, and then start it as a http server
    def start_app(self):
        self.connection = connect(TEST_DB_NAME)
        app = api.make_app()

        def run():
            app.listen(8080)
            tornado.ioloop.IOLoop.instance().start()

        # to start it async we need to use threads
        # otherwise the script will not return unless tornado ioloop stops;
        # which is not what we want
        threading.Thread(target=run).start()

    # stop the running app
    def stop_app(self):
        # get the current ioloop instance of tornado and stop it
        tornado.ioloop.IOLoop.instance().stop()

    # load the test data from a file
    def load_test_data(self):
        curr_path = os.path.dirname(os.path.realpath(__file__))
        fp = open(os.path.join(curr_path, 'test_data.json'), 'r')
        self.test_data = json.load(fp)
        fp.close()

    # insert data to the db
    def insert_data(self, data):
        new_lab = Lab(**data)
        new_lab.save()

    # drop the lab collection
    def drop_lab_collection(self):
        Lab.drop_collection()

    # initial setup
    def setUp(self):
        print 'setUp()'
        self.load_test_data()
        self.start_app()

    def tearDown(self):
        print 'tearDown()'
        self.stop_app()
        self.connection.drop_database(TEST_DB_NAME)

    #def test_Lab_Id(self):
    #    r = requests.get('http://localhost:8080/labs/547d5cae3e56404101173170').json()
    #    print (json.dumps(r))
    #    expected_data = '{"status": "Hosted", "lab_id": "cse01", "hosted_url": "http://virtual-labs.ac.in/labs/cse01/", "auto_hostable": "Yes", "type_of_lab": "", "simulation": "Yes", "content": "Yes", "lab_name": "Data Structures", "sources_available": "Yes", "repo_url": "https://bitbucket.org/virtual-labs/cse01-ds_new", "discipline_name": "cse", "remarks": "Completed ", "integration_level": 5, "id": "547d5cae3e56404101173170"}'
    #    self.assertEqual(json.dumps(r), expected_data)

    #def test_Discipline(self):
    #    r = requests.get('http://localhost:8080/labs/discipline/ece').json()
    #    print (json.dumps(r))
    #    expected_data = '[{"auto_hostable": "Yes", "lab_id": "cse02", "_id": {"$oid": "547d5cae3e56404101173171"}, "hosted_url": "http://virtual-labs.ac.in/labs/cse02/", "number_of_experiments": 10, "type_of_lab": "", "institute_id": 4, "simulation": "Yes", "content": "Yes", "lab_name": "Computer Programming", "lab_deployed": "Yes", "sources_available": "Yes", "status": "Hosted", "repo_url": "https://bitbucket.org/virtual-labs/cse02-programming", "discipline_name": "ece", "remarks": "Completed ", "developer": "jawahar@iiit.ac.in", "integration_level": 5, "id": 2, "web2.0_compliance": "No"}]'
    #    self.assertEqual(json.dumps(r), expected_data)

    def test_get_all_labs(self):
        print "test get all labs()"
        for lab in self.test_data:
            self.insert_data(lab)

        resp = requests.get('http://localhost:8080/labs')
        #print resp.text
        resp_data = json.loads(resp.text)
        #print type(resp_data['labs'])
        #print type(self.test_data)
        self.assertEqual(len(self.test_data), len(resp_data['labs']))

        self.assertEqual(self.test_data[0]['lab_name'],
                         resp_data['labs'][0]['lab_name'])

        self.assertEqual(self.test_data[1]['discipline_name'],
                         resp_data['labs'][1]['discipline_name'])

        self.drop_lab_collection()


if __name__ == '__main__':
    unittest.main()
