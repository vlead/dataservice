# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app

import re

from utils import typecheck

db = SQLAlchemy()


class Version(object):
    pass


class URL(object):
    pass


class Name(object):
    def __init__(self, value):
        # if the string contains any non-alphabet and non-space character, raise
        # a type error
        if re.search('[^a-zA-Z ]+', value):
            raise TypeError('%s is not a Name!' % value)

        self.value = value

    # def __str__(self):
    #    return self.value

    # def __repr__(self):
    #    return self.value


class InstituteName(object):
    def __init__(self, value):
        # if the string contains any non-alphabet, non-hyphen and non-space
        # character, raise a type error
        if re.search('[^a-zA-Z\- ]+', value):
            raise TypeError('%s is not a Name!' % value)

        self.value = value


class Email(object):
    def __init__(self, value):
        if not re.search('[^@]+@[^@]+\.[^@]+', value):
            raise TypeError('%s is not an email_id!' % value)
        self.value = value


# Abstract class to hold common methods
class Entity(db.Model):

    __abstract__ = True

    # save a db.Model to the database. commit it.
    def save(self):
        db.session.add(self)
        db.session.commit()

    # update the object, and commit to the database
    def update(self, **kwargs):
        for attr, val in kwargs.iteritems():
            self.__setattr__(attr, val)

        self.save()


class Institute(Entity):

    __tablename__ = 'institutes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    pic = db.Column(db.String(128))
    iic = db.Column(db.String(128))

    labs = db.relationship('Lab', backref='institute')

    @staticmethod
    def get_all():
        return [i.to_client() for i in Institute.query.all()]

    def get_id(self):
        return self.id

    # def get_institute_mnemonic(self):
        # return self.mnemonic

    def get_name(self):
        return self.name

    def get_pic(self):
        return self.pic

    def get_iic(self):
        return self.iic

    @staticmethod
    # TODO: Add same get for a mnemonic too
    def get_institute_by_id(id):
        return Institute.query.get(id)

    @typecheck(name=InstituteName)
    def set_name(self, name):
        self.name = name

    @typecheck(pic=Name)
    def set_pic(self, pic):
        self.pic = pic

    @typecheck(iic=Name)
    def set_iic(self, iic):
        self.iic = iic

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'pic': self.pic,
            'iic': self.iic
        }


class Discipline(Entity):

    __tablename__ = 'disciplines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    dnc = db.Column(db.String(64))

    labs = db.relationship('Lab', backref='discipline')

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'dnc': self.dnc
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in Discipline.query.all()]

    @staticmethod
    def get_discipline_name(id):
        return Discipline.query.get(id)

    def get_discipline_id(self):
        return self.id

    def get_discipline_dnc(self):
        return self.dnc

    @typecheck(dnc=Name)
    def set_discipline_dnc(self, dnc):
        self.dnc = dnc.value

    """
    def get_mnemonic(self):
        return self.mnemonic
    """


class Lab(Entity):

    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    mnemonic = db.Column(db.String(32), nullable=False)
    slug = db.Column(db.String(128))

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))

    integration_level_id = db.Column(db.ForeignKey('integration_levels.id'))
    integration_level = db.relationship('IntegrationLevel')

    number_of_experiments = db.Column(db.Integer)

    repo_url = db.Column(db.String(256))

    hosted_url = db.Column(db.String(256))

    hosted_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))
    hosted_on = db.relationship('HostingPlatform')

    type_of_lab_id = db.Column(db.ForeignKey('type_of_labs.id'))
    type_of_lab = db.relationship('TypeOfLab')

    remarks = db.Column(db.Text)
    status = db.Column(db.String(32))

    is_web_2_compliant = db.Column(db.Boolean)
    is_phase_2_lab = db.Column(db.Boolean)

    @staticmethod
    def get_all(fields=None):
        # get all labs from db
        labs = [i.to_client() for i in Lab.query.all()]
        print 'total count of labs'
        print len(labs)
        # print fields
        # if request do not contain fields, return the data
        if not fields:
            return labs
        # if fields exist in the request, format all the labs to have only the
        # fields requested by the user
        formatted_labs = Lab.format_labs_by_fields(labs, fields)
        return formatted_labs

    @staticmethod
    def get_specific_lab(id, fields=None):
        # get the lab from the db
        lab = Lab.query.get(id)
        # if lab does not exist
        if not lab:
            return None
        lab = lab.to_client()
        # if request do not contain fields, return the data
        if not fields:
            return lab
        # if fields exist in the request, format the lab to have only the
        # fields requested by the user
        formatted_lab = Lab.format_labs_by_fields([lab], fields)[0]
        return formatted_lab

    @staticmethod
    def format_labs_by_fields(labs, fields):
        current_app.logger.debug("labs recvd: %s" % labs)
        formatted_labs = []  # all labs
        for lab in labs:
            formatted_lab = {}  # formatted lab
            for field in fields:
                try:
                    formatted_lab[field] = lab[field]
                except KeyError:
                    raise Exception('Invalid field %s', field)

            # print fmttd_lab
            formatted_labs.append(formatted_lab)
        return formatted_labs

    def to_client(self):
        return {
            'id': self.id,
            'mnemonic': self.mnemonic,
            'name': self.name,
            'slug': self.slug,
            'institute': self.institute.to_client(),
            'discipline': self.discipline.to_client(),
            'integration_level': self.integration_level,
            'number_of_experiments': self.number_of_experiments,
            'repo_url': self.repo_url,
            'hosted_url': self.hosted_url,
            'hosted_on': self.hosted_on,
            'technologies': self.get_technologies(),
            'developers': self.get_developers(),
            'type_of_lab': self.type_of_lab,
            'status': self.status,
            'is_web_2_compliant': self.is_web_2_compliant,
            'is_phase_2_lab': self.is_phase_2_lab,
            'remarks': self.remarks
        }


class Developer(Entity):

    __tablename__ = 'developers'

    id = db.Column(db.Integer, primary_key=True)

    email_id = db.Column(db.String(128))
    name = db.Column(db.String(64), nullable=False)

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    institute = db.relationship('Institute')

    @staticmethod
    def get_all():
        return [i.to_client() for i in Developer.query.all()]

    def get_id(self):
        return self.id

    @staticmethod
    def get_developer(id):
        return Developer.query.get(id)

    def get_email(self):
        return self.email_id

    def get_name(self):
        return self.name

    @typecheck(name=Name)
    def set_name(self, name):
        self.name = name.value

    @typecheck(email_id=Email)
    def set_email(self, email_id):
        self.email_id = email_id.value

    def to_client(self):
        return {
            'id': self.id,
            'email_id': self.email_id,
            'name': self.name,
            'institute': self.institute.to_client()
        }


class Technology(Entity):

    __tablename__ = 'technologies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    version = db.Column(db.String(32))
    foss = db.Column(db.Boolean)

    @staticmethod
    def get_all():
        return [i.to_client() for i in Technology.query.all()]

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'foss': self.foss
        }


class HostingPlatform(Entity):
    __tablename__ = 'hosting_platforms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)


class Experiment(Entity):

    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True)

    # Our data set has really, really long experiment names and URLs!!
    name = db.Column(db.String(256))

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    content_url = db.Column(db.String(256))
    # content_on = db.Column(db.Enum('CPE', 'ELSE', 'NA'))
    content_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))
    content_on = db.relationship('HostingPlatform')

    simulation_url = db.Column(db.String(256))
    # simulation_on = db.Column(db.Enum('CPE', 'ELSE', 'NA'))
    simulation_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))
    simulation_on = db.relationship('HostingPlatform')

    @typecheck(lab=Lab, content_url=URL, content_hosted_on=HostingPlatform,
               simulation_url=URL, simulation_hosted_on=HostingPlatform)
    def __init__(self, **kwargs):
        # TODO: implement the constructor and check the validity!
        pass

    def get_id(self):
        return self.id

    @staticmethod
    def get_experiment(id):
        return Experiment.query.get(id)

    def get_content_url(self):
        return self.content_url

    def get_simulation_url(self):
        return self.simulation_url

    def content_hosted_on(self):
        return self.content_hosted_on

    def simulation_hosted_on(self):
        return self.simulation_hosted_on

    def get_lab(self):
        return self.lab

    @typecheck(url=URL)
    def set_content_url(self, url):
        self.content_url = url

    def set_simulation_url(self, url):
        self.simulation_url = url

    @typecheck(platform=HostingPlatform)
    def set_content_hosted_on(self, platform):
        self.content_hosted_on = platform

    @typecheck(platform=HostingPlatform)
    def set_simulation_hosted_on(self, platform):
        self.simulation_hosted_on = platform

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'content_url': self.content_url,
            'content_on': self.content_on,
            'simulation_url': self.simulation_url,
            'simulation_on': self.simulation_on,
            'lab': self.lab.to_client()
        }


class IntegrationLevel(Entity):
    __tablename__ = 'integration_levels'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)


class TypeOfLab(Entity):
    __tablename__ = 'type_of_labs'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)


class LabSystemInfo(Entity):

    __tablename__ = 'labs_system_info'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    storage = db.Column(db.String(64))
    memory = db.Column(db.String(64))

    arch = db.Column(db.String(64))
    os = db.Column(db.String(64))
    os_version = db.Column(db.String(64))

    hosting = db.Column(db.String(64))
    vm_id = db.Column(db.String(64))
    ip_addr = db.Column(db.String(64))

    def to_client(self):
        return {
            # 'lab': self.lab.to_client(),
            'lab': {
                'id': self.lab.id,
                'name': self.lab.name
            },
            'id': self.id,
            'storage': self.storage,
            'memory': self.memory,
            'os': self.os,
            'os_version': self.os_version,
            'arch': self.arch,
            'hosting': self.hosting,
            'vm_id': self.vm_id,
            'ip_addr': self.ip_addr,
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in LabSystemInfo.query.all()]

if __name__ == "__main__":
    print Discipline.get_disc("1")
    print Discipline.get_dnc()
