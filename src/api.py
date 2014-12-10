# -*- coding: utf-8 -*-
# API Layer
# Data Service
# Lab and Related Services
# Virtual Labs Platform


import tornado.httpserver
import tornado.options
import tornado.web

from tornado.options import define
#from bson.objectid import ObjectId
from db import *


define("port", default=8080, help="run on the given the port", type=int)


class LabHandler(tornado.web.RequestHandler):
    # executes when GET method is recvd
    # fields are expected as ?fields=<field1>&fields=<field2>.. convention
    def get(self):
        # get the fields attributes from query string
        fields = self.get_query_arguments('fields')
        print fields
        try:
            self.finish({'labs': Lab.getAllLabs(fields)})
        except:
            self.set_status(400)
            self.finish({'error': 'Invalid field attribute'})

    # POST Method for /labs
    # Create a new lab
    def post(self):
        err = None
        if not self.get_body_argument('lab_name'):
            err = 'Field lab_name cannot be empty'

        if not self.get_body_argument('institute_name'):
            err = 'Field institute_name cannot be empty'

        if not self.get_body_argument('discipline_name'):
            err = 'Field discipline_name cannot be empty'

        if not self.get_body_argument('repo_url'):
            err = 'Field repo_url cannot be empty'

        if err:
            self.set_status(400)
            self.finish({"error": err})

        args = {}
        for field in self.request.arguments:
            args[field] = self.get_body_argument(field)
        
        new_lab = Lab(**args)
        new_lab.save()
        self.finish(new_lab.to_client())

   
class LabIdHandler(tornado.web.RequestHandler):
    def get(self, _id, param=None):
        # get the specific lab passed from ID passed in the URL
        lab = Lab.getLabById(_id)
        if lab:
            # if further param/field is present
            if param:
                try:
                    # filter by it
                    self.finish({param: lab[param]})
                except KeyError:
                    # else invalid field
                    self.finish({'error': 'Invalid field attribute'})

            else:
                self.finish(lab.to_client())
        else:
            self.set_status(404)
            self.finish({"error": "Lab not found"})

    # PUT method for /labs
    # Update an existing lab identified by lab_id
    def put(self, lab_id, param=None):
        #lab = Lab.objects(__raw__={"_id": ObjectId(lab_id)})[0]
        lab = Lab.getLabById(lab_id)
        #print(self.request.arguments)
        for field in self.request.arguments:
            lab[field] = self.get_body_argument(field)

        print 'updated lab ' + lab_id
        print lab.to_dict()

        lab.save()
        self.finish({'updated_lab': lab.to_client()})


class LabDisciplineHandler(tornado.web.RequestHandler):
    def get(self, disciplinename):
        sub_coll = Lab.objects(discipline_name=disciplinename).to_json()
        if sub_coll:
            self.write(sub_coll)
        else:
            self.set_status(404)
            self.write({"error": "Details not found with specified discipline"})


class LabInstituteHandler(tornado.web.RequestHandler):
    def get(self, instt_name, disc_name=None):
        print 'incoming instt name'
        print instt_name
        labs = Lab.objects(institute_name=instt_name)
        if disc_name:
            print disc_name
            labs = labs.filter(discipline_name=disc_name)
        print labs
        if len(labs):
            self.finish({'labs': map(lambda x: x.to_client(), labs)})
        else:
            self.set_status(404)
            self.finish({'error': 'Institute not found'})


class LabSearchHandler(tornado.web.RequestHandler):
    def get(self):
        search = {}
        for field in self.request.arguments:
            search[field] = self.get_query_argument(field)
            print search

            labs = Lab.objects(__raw__=search)
            if len(labs):
                self.finish({'labs': map(lambda x: x.to_client(), labs)})

            else:
                self.set_status(400)
                self.finish({'error': 'No lab found'})


#class InstituteHandler(tornado.web.RequestHandler):
#    def post(self):
#        err = None


class InstituteHandler(tornado.web.RequestHandler):
    def get(self):
	coll = Institute.objects().to_json()
        try:
            self.finish(coll)
        except:
            self.set_status(400)
            self.finish({'error': 'Institute Collection does not exits in db'})
class DisciplineHandler(tornado.web.RequestHandler):
    def get(self):
        coll = Discipline.objects().to_json()
        try:
            self.finish(coll)
        except:
            self.set_status(400)
            self.finish({'error': 'Discipline collection does not exits in db'})

def make_app():
    return tornado.web.Application([
        tornado.web.url(r'/labs/?', LabHandler),
        tornado.web.url(r'/labs/discipline/([a-z]*)', LabDisciplineHandler),
        tornado.web.url(r'/labs/institute/(\w+)/?discipline/?(\w+)?',
                        LabInstituteHandler),
        tornado.web.url(r'/labs/search', LabSearchHandler),
        tornado.web.url(r'/labs/([0-9a-z]*)/?(\w+)?', LabIdHandler),
	tornado.web.url(r'/institutes', InstituteHandler),
        tornado.web.url(r'/disciplines', DisciplineHandler)
    ])

