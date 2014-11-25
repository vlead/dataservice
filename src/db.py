# -*- coding: utf-8 -*-
# data layer

from mongoengine import *
from bson.objectid import ObjectId
import json

connection = connect('labs-info')


#TODO: refine the member variables
class Lab(Document):
    lab_id = StringField()
    institute_name = StringField()
    lab_name = StringField()
    #name = StringField()
    discipline_name = StringField()
    developers = StringField()
    repo_url = StringField()
    sources_available = StringField()
    hosted_url = StringField()
    is_deployed = StringField()
    num_of_exps = IntField()
    content = StringField()
    simulation = StringField()
    web_2_compliance = StringField()
    type_of_lab = StringField()
    auto_hostable = StringField()
    remarks = StringField()
    integration_level = IntField()
    status = StringField()

    @staticmethod
    # take id as a string and return the lab corresponding to that id
    def getLabById(_id):
        return Lab.objects(id=ObjectId(_id))[0]

    @staticmethod
    def getAllLabs(fields):
        if fields:
            labs = []
            # loop over each lab in the whole collection
            for lab in Lab.objects:
                # filtered lab object
                fmt_lab = {}
                # loop over the passed fields
                for field in fields:
                    try:
                        # append the values if they exist
                        fmt_lab[field] = lab[field]
                    except:
                        # raise an excep if doesnt
                        raise Exception('Invalid Field')
                # append formatted labs
                labs.append(fmt_lab)
            return labs

        # if no fields options passed; return all fields
        return map(lambda x: x.to_client(), Lab.objects)

    # return a dictionary format of the labs members..
    def to_dict(self):
        return json.loads(self.to_json())

    # return a JSON(string) with fields relevant to the client
    def to_client(self):
        lab_dict = json.loads(self.to_json())
        del(lab_dict['_id'])
        lab_dict['id'] = unicode(self.id)
        #return json.dumps(lab_dict)
        return lab_dict

