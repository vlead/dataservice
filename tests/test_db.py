
import unittest
from mongoengine import connect
import os
import json

from src.db import Lab


class TestDB(unittest.TestCase):

    def setUp(self):
        self.connection = connect('test-labs-db')
        path = os.path.dirname(os.path.realpath(__file__))
        fp = open(os.path.join(path, 'test_data.json'), 'r')
        self.test_data = json.load(fp)
        fp.close()

    def tearDown(self):
        #TODO: drop database and close connection
        self.connection.drop_database('test-labs-db')

    def test_get_all_labs_wo_fields(self):
        for lab in self.test_data:
            new_lab = Lab(**lab)
            new_lab.save()

        all_labs = Lab.getAllLabs(None)

        for lab in all_labs:
            del(lab['id'])

        print "test data"
        print self.test_data
        print "all labs"
        print all_labs

        self.assertEqual(len(all_labs), len(self.test_data))

    def test_get_all_fields(self):
        #TODO: write test for get all labs passing fields parameters


if __name__ == '__main__':
    unittest.main()
