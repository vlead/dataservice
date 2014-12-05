import unittest
import requests
import subprocess
import json
import os

from src.db import Lab
from src import test_app


class TestAPI(unittest.TestCase):
    # helper functions
    def insert_data(self, data):
        new_lab = Lab(**data)
        new_lab.save()

    def drop_collection(self):
        Lab.drop_collection()

    # initial setup
    def setUp(self):
        print 'setUp()'
        curr_path = os.path.dirname(os.path.realpath(__file__))
        self.proc = subprocess.Popen(["nohup", "python", "src/test_app.py"])
        fp = open(os.path.join(curr_path, 'test_data.json'), 'r')
        self.test_data = json.load(fp)
        fp.close()

    def tearDown(self):
        print 'tearDown()'
        self.proc.terminate()

    def test_Lab_Id(self):
        r = requests.get('http://localhost:8080/labs/547d5cae3e56404101173170').json()
        print (json.dumps(r))
        expected_data = '{"status": "Hosted", "lab_id": "cse01", "hosted_url": "http://virtual-labs.ac.in/labs/cse01/", "auto_hostable": "Yes", "type_of_lab": "", "simulation": "Yes", "content": "Yes", "lab_name": "Data Structures", "sources_available": "Yes", "repo_url": "https://bitbucket.org/virtual-labs/cse01-ds_new", "discipline_name": "cse", "remarks": "Completed ", "integration_level": 5, "id": "547d5cae3e56404101173170"}'
        self.assertEqual(json.dumps(r), expected_data)

    def test_Discipline(self):
        r = requests.get('http://localhost:8080/labs/discipline/ece').json()
        print (json.dumps(r))
        expected_data = '[{"auto_hostable": "Yes", "lab_id": "cse02", "_id": {"$oid": "547d5cae3e56404101173171"}, "hosted_url": "http://virtual-labs.ac.in/labs/cse02/", "number_of_experiments": 10, "type_of_lab": "", "institute_id": 4, "simulation": "Yes", "content": "Yes", "lab_name": "Computer Programming", "lab_deployed": "Yes", "sources_available": "Yes", "status": "Hosted", "repo_url": "https://bitbucket.org/virtual-labs/cse02-programming", "discipline_name": "ece", "remarks": "Completed ", "developer": "jawahar@iiit.ac.in", "integration_level": 5, "id": 2, "web2.0_compliance": "No"}]'
        self.assertEqual(json.dumps(r), expected_data)

    def test_all_labs(self):
        print "test labs()"
        for lab in self.test_data:
            self.insert_data(lab)

        resp = requests.get('http://localhost:8080/labs')
        #print resp.text
        resp_data = json.loads(resp.text)
        #print type(resp_data['labs'])
        #print type(self.test_data)
        self.assertEqual(len(self.test_data), len(resp_data['labs']))

        self.drop_collection()


if __name__ == '__main__':
    unittest.main()
