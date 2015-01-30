from flask import Flask
import json
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Lab(db.Model):

    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.String(45))
    lab_name = db.Column(db.String(100))
    discipline_id = db.Column(db.String(100), db.ForeignKey('disciplines.id'))
    discipline = db.relationship('Discipline')
    developer = db.Column(db.String(100), db.ForeignKey('developers.email_id'))
    developer_obj = db.relationship('Developer')
    repo_url = db.Column(db.String(200))
    sources_available = db.Column(db.String(45))
    hosted_url = db.Column(db.String(200))
    lab_deployed = db.Column(db.String(45))
    number_of_experiments = db.Column(db.Integer)
    content = db.Column(db.String(45))
    simulation = db.Column(db.String(45))
    web_2_compliance = db.Column('web2.0_compliance', db.String(45))
    type_of_lab = db.Column(db.String(45))
    auto_hostable = db.Column(db.String(45))
    remarks = db.Column(db.String(200))
    integration_level = db.Column(db.Integer)
    status = db.Column(db.String(45))
    institute_id = db.Column(db.Integer,db.ForeignKey('institutes.id'))
    institute = db.relationship('Institute')
    phase_2_lab = db.Column(db.String(45))

    def to_client(self):
	return {
	   'lab_id': self.lab_id,
	   'lab_name':self.lab_name,
           'institute':{
		'id': self.institute.id,
                'institute_name': self.institute.institute_name,
                'institute_coordinator': self.institute.institute_coordinators,
		'institute_integration_coordinator':self.institute.institute_integration_coordinators
	    },
	   'discipline': {
	        'discipline_name':self.discipline.discipline_name,
	        'dnc':self.discipline.dnc
	    },
            'developer': {
		'name': self.developer_obj.developer_name,
		'email': self.developer_obj.email_id
	    },
	   'repo_url':self.repo_url,
	
	  'sources_available':self.sources_available,
	  'hosted_url':self.hosted_url,
	  'lab_deployed':self.lab_deployed,
	  'number_of_experiments':self.number_of_experiments,
	  'content':self.content,
	  'simulation':self.simulation,
	  'web_2_compliance':self.web_2_compliance,
          'type_of_lab':self.type_of_lab,
          'auto_hostable':self.auto_hostable,
          'remarks':self.remarks,
          'integration_level':self.integration_level,
	  'status':self.status,
	  'phase_2_lab':self.phase_2_lab
        } 
	

    @staticmethod
    def getAllLabs(fields):
        #four i in Lab.query.all():
            #return (i.__dict__)
	return [i.to_client() for i in Lab.query.all()]
        
class Institute(db.Model):

    __tablename__ = 'institutes'

    id = db.Column(db.Integer, primary_key=True)
    institute_name = db.Column(db.String(45))
    institute_coordinators = db.Column(db.String(100))
    institute_integration_coordinators = db.Column(db.String(100))

    @staticmethod
    def getAllInstitutes(fields):
        for i in Institute.query.all():
            return (i.__dict__)


class Discipline(db.Model):
    __tablename__ = 'disciplines'

    id = db.Column(db.Integer)
    discipline_name = db.Column(db.String(100), primary_key=True)
    dnc = db.Column(db.String(50))

    @staticmethod
    def getAllDisciplines(fields):
        for i in Discipline.query.all():
            return (i.__dict__)



class Developer(db.Model):

    __tablename__ = 'developers'

    email_id = db.Column(db.String(100), primary_key=True)
    developer_name = db.Column(db.String(100))
    institute_name = db.Column(db.String(45))


class DevelopersEngaged(db.Model):

    __tablename__ = 'developers_engaged'

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    developer_id = db.Column(db.String(100), db.ForeignKey('developers.email_id'))

class Technology(db.Model):
 
    __tablename__ = 'technologies'

    id = db.Column(db.Integer, primary_key=True)
    technology_name = db.Column(db.String(100))
    foss = db.Column(db.String(100))


class Technology_Used(db.Model):

    __tablename__ = 'technologies_used'

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab_id = db.Column(db.Integer, db.ForeignKey('technologies.id'))
    technology_name = db.Column(db.String(100))
    foss = db.Column(db.String(100))

