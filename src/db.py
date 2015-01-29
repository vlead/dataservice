
# -*- coding: utf-8 -*-
# Data Layer
# Data Service
# Lab and Related Services
# Virtual Labs Platform


from mongoengine import *
from bson.objectid import ObjectId
import json


#TODO: refine the member variables
class Lab(Document):
    lab_id = StringField()
    institute =  ReferenceField('Institute')
    name =  StringField(required=True)
    discipline =  ReferenceField('Discipline')
    developers = ListField(ReferenceField('Developer'))
    technologies_used = ListField(ReferenceField('Technology'))
    repo_url =  StringField(required=True)
    sources_available = StringField()
    hosted_url = StringField()
    is_deployed = BooleanField()
    num_of_exps = IntField()
    is_content = BooleanField()
    is_simulation = BooleanField()
    web_2_compliance = StringField()
    type_of_lab = StringField()
    auto_hostable = StringField()
    remarks = StringField()
    integration_level = IntField()
    status = StringField()

    @staticmethod
    def createNew(**kwargs):
        instt = Institute.objects(name=kwargs['institute_name'])[0]
	# filter returns back a list 
	print instt.to_json()
	kwargs['institute_name'] = instt
        disc = Discipline.objects(name=kwargs['discipline_name'])[0]
	print disc.to_json()
	kwargs['discipline_name'] = disc
	print "saving reference.."
	new_lab = Lab(**kwargs)
	print kwargs
	print new_lab.to_json()
	new_lab.save()
  	return new_lab	
#	disc = Discipline.objects(name=kwargs['discipline_name'])
 #       self.discipline_name = disc.

#    @staticmethod 
#    def updateNew(field,lab):
#        print "entering...."
#	print field
#        instt = Institute.objects(name='field')[0]
#	print instt
#        print instt.to_json()
#        lab['institute_name'] = instt
#            print "entering elif..."
#            disc = Discipline.objects(name=field)[0]
#            print disc.to_json()
#            lab['discipline_name'] = disc

#	lab.save()
#	print updated_lab.to_json()
 #       return lab


	

    @staticmethod
    # take id as a string and return the lab corresponding to that id
    def getLabById(_id):
        try:
            return Lab.objects(id=ObjectId(_id))[0]
        except IndexError:
            return False

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

    # return a dict with fields relevant to the client
    def to_client(self):
        lab_dict = json.loads(self.to_json())
        del(lab_dict['_id'])
        lab_dict[u'id'] = unicode(self.id)
	lab_dict[u'institute_name']= unicode(self.institute_name.name)
	lab_dict[u'discipline_name']= unicode(self.discipline_name.name)
        #return json.dumps(lab_dict)
        return lab_dict


class Institute(Document):
    name = StringField(required=True)
    coordinators = StringField()
    integration_coordinators = StringField()	
    
    
class Discipline(Document):
     name = StringField(required=True)
     dnc = StringField()	

class Developer(Document):	
    email_id  =StringField(required=True)
    developer_name = StringField()
    institute_name =  StringField()

class Experiment(Document):
    exp_id=IntField(required=True)
    exp_name=StringField()
    content_url=StringField()
    simulation_url=StringField()

class Technology(Document):
    name=StringField()
    foss=StringField()






    

    
    

