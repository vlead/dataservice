import unittest
import requests
import api
import subprocess
import app
import json

class MyTest(unittest.TestCase):
    def setUp(self):
        self.proc = subprocess.Popen(["nohup", "python", "app.py"])
    def tearDown(self):
        self.proc.terminate()
    def testLabId(self):
        r = requests.get('http://localhost:8080/labs/547d5cae3e56404101173170').json()
        print (json.dumps(r))
        expected_data = '{"status": "Hosted", "lab_id": "cse01", "hosted_url": "http://virtual-labs.ac.in/labs/cse01/", "auto_hostable": "Yes", "type_of_lab": "", "simulation": "Yes", "content": "Yes", "lab_name": "Data Structures", "sources_available": "Yes", "repo_url": "https://bitbucket.org/virtual-labs/cse01-ds_new", "discipline_name": "cse", "remarks": "Completed ", "integration_level": 5, "id": "547d5cae3e56404101173170"}'
        self.assertEqual(json.dumps(r),expected_data)
    def testDiscipline(self):
        r = requests.get('http://localhost:8080/labs/discipline/ece').json()
        print (json.dumps(r))
        expected_data = '[{"auto_hostable": "Yes", "lab_id": "cse02", "_id": {"$oid": "547d5cae3e56404101173171"}, "hosted_url": "http://virtual-labs.ac.in/labs/cse02/", "number_of_experiments": 10, "type_of_lab": "", "institute_id": 4, "simulation": "Yes", "content": "Yes", "lab_name": "Computer Programming", "lab_deployed": "Yes", "sources_available": "Yes", "status": "Hosted", "repo_url": "https://bitbucket.org/virtual-labs/cse02-programming", "discipline_name": "ece", "remarks": "Completed ", "developer": "jawahar@iiit.ac.in", "integration_level": 5, "id": 2, "web2.0_compliance": "No"}]'
        self.assertEqual(json.dumps(r), expected_data)


if __name__ == '__main__':
    unittest.main()

