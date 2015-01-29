from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lab(db.Model):

    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.String(45))
    #institute_name = db.Column(db.String(45))
    lab_name = db.Column(db.String(100))
    discipline_id = db.Column(db.String(100), db.ForeignKey('disciplines.id'))
    discipline = db.relationship('Discipline')
    developer = db.Column(db.String(100), db.ForeignKey('developers.email_id'))
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

    @staticmethod
    def getAllLabs(fields):
       # if fields:
	    
	#else:
        return Lab.query.all()  

class Institute(db.Model):
    __tablename__ = 'institutes'

    id = db.Column(db.Integer, primary_key=True)
    institute_name = db.Column(db.String(45))
    institute_coordinators = db.Column(db.String(100))

class Discipline(db.Model):
    __tablename__ = 'disciplines'

    id = db.Column(db.Integer)
    discipline_name = db.Column(db.String(100), primary_key=True)
    dnc = db.Column(db.String(50))

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



