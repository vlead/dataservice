# -*- coding: utf-8 -*-
# data layer

from mongoengine import *

connection = connect('labs-info')


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
