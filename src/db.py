# -*- coding: utf-8 -*-
# data layer

from mongoengine import *

connection = connect('labs-info')


#TODO: refine the member variables
class Lab(Document):
    lab_id = StringField()
    insitute_name = StringField()
    lab_name = StringField()
    discipline_name = StringField()
    developers = StringField()
    repo_url = StringField()
    sources_available = StringField()
    hosted_url = StringField()
    lab_deployed = StringField()
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
    def getAllLabs():
        return map(lambda x: x.to_json(), Lab.objects)
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
        return map(lambda x: x.to_json(), Lab.objects)
