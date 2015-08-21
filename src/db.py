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
    mnemonic = db.Column(db.String(16), nullable=False)
    pic = db.Column(db.String(128))
    iic = db.Column(db.String(128))

    labs = db.relationship('Lab', backref='institute')
    developers = db.relationship('Developer', backref='institute')

    @staticmethod
    def get_all():
        return [i.to_client() for i in Institute.query.all()]

    # TODO: Add same get for a mnemonic too
    @staticmethod
    def get_institute_by_id(id):
        return Institute.query.get(id)
        
    def get_id(self):
        return self.id

    def get_mnemonic(self):
        return self.mnemonic

    def get_name(self):
        return self.name

    def get_pic(self):
        return self.pic

    def get_iic(self):
        return self.iic

    def get_labs(self):
        return self.labs
    
    @typecheck(name=InstituteName)
    def set_name(self, name):
        self.name = name.value
        self.save()

    @typecheck(pic=Name)
    def set_pic(self, pic):
        self.pic = pic.value
        self.save()

    @typecheck(iic=Name)
    def set_iic(self, iic):
        self.iic = iic.value
        self.save()

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'mnemonic': self.mnemonic,
            'pic': self.pic,
            'iic': self.iic
        }


class Discipline(Entity):

    __tablename__ = 'disciplines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    mnemonic = db.Column(db.String(16), nullable=False)
    dnc = db.Column(db.String(64))

    labs = db.relationship('Lab', backref='discipline')

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'mnemonic': self.mnemonic,
            'dnc': self.dnc
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in Discipline.query.all()]

    # TODO: Add same get for a mnemonic too
    @staticmethod
    def get_discipline_by_id(id):
        return Discipline.query.get(id)

    def get_id(self):
        return self.id

    def get_mnemonic(self):
        return self.mnemonic

    def get_name(self):
        return self.name

    def get_dnc(self):
        return self.dnc

    def get_labs(self):
        return self.labs

    @typecheck(name=Name)
    def set_name(self, name):
        self.name = name.value
        self.save()

    @typecheck(dnc=Name)
    def set_dnc(self, dnc):
        self.dnc = dnc.value
        self.save()


class Developer(Entity):

    __tablename__ = 'developers'

    id = db.Column(db.Integer, primary_key=True)

    email_id = db.Column(db.String(128))
    name = db.Column(db.String(64), nullable=False)

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))

    @staticmethod
    def get_all():
        return [i.to_client() for i in Developer.query.all()]

    @staticmethod
    def get_developer(id):
        return Developer.query.get(id)

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email_id

    def get_name(self):
        return self.name

    def get_labs(self):
        return self.labs

    @typecheck(name=Name)
    def set_name(self, name):
        self.name = name.value
        self.save()

    @typecheck(email_id=Email)
    def set_email(self, email_id):
        self.email_id = email_id.value
        self.save()

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

    labs = db.relationship('Lab', backref='hosted_on')


# association table of developers and labs
developers_engaged = db.Table(
    'developers_engaged',
    db.Column('lab_id', db.Integer, db.ForeignKey('labs.id')),
    db.Column('developer_id', db.Integer, db.ForeignKey('developers.id'))
)

# association table of technologies and labs
technologies_used_labs = db.Table(
    'technologies_used_labs',
    db.Column('lab_id', db.Integer, db.ForeignKey('labs.id')),
    db.Column('tech_id', db.Integer, db.ForeignKey('technologies.id'))
)

# association table of technologies and experiments
technologies_used_expt = db.Table(
    'technologies_used_expt',
    db.Column('expt_id', db.Integer, db.ForeignKey('experiments.id')),
    db.Column('tech_id', db.Integer, db.ForeignKey('technologies.id'))
)


class Experiment(Entity):

    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True)

    # Our data set has really, really long experiment names and URLs!!
    name = db.Column(db.String(256))

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))

    content_url = db.Column(db.String(256))
    # content_on = db.Column(db.Enum('CPE', 'ELSE', 'NA'))
    content_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))
    content_on = db.relationship('HostingPlatform',
                                 foreign_keys=[content_on_id])

    simulation_url = db.Column(db.String(256))
    # simulation_on = db.Column(db.Enum('CPE', 'ELSE', 'NA'))
    simulation_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))
    simulation_on = db.relationship('HostingPlatform',
                                    foreign_keys=[simulation_on_id])

    technologies = db.relationship('Technology',
                                   secondary=technologies_used_expt,
                                   backref='experiments')

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
        self.save()

    @typecheck(url=URL)
    def set_simulation_url(self, url):
        self.simulation_url = url
        self.save()

    @typecheck(platform=HostingPlatform)
    def set_content_hosted_on(self, platform):
        self.content_hosted_on = platform
        self.save()

    @typecheck(platform=HostingPlatform)
    def set_simulation_hosted_on(self, platform):
        self.simulation_hosted_on = platform
        self.save()

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

    labs = db.relationship('Lab', backref='integration_level')


class TypeOfLab(Entity):
    __tablename__ = 'type_of_labs'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)

    labs = db.relationship('Lab', backref='type_of_lab')


class Lab(Entity):

    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    mnemonic = db.Column(db.String(16), nullable=False)
    slug = db.Column(db.String(128))

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))

    integration_level_id = db.Column(db.ForeignKey('integration_levels.id'))

    developers = db.relationship('Developer', secondary=developers_engaged,
                                 backref='labs')

    number_of_experiments = db.Column(db.Integer)

    experiments = db.relationship('Experiment', backref='lab')

    technologies = db.relationship('Technology',
                                   secondary=technologies_used_labs,
                                   backref='labs')

    repo_url = db.Column(db.String(256))

    hosted_url = db.Column(db.String(256))

    hosted_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))

    type_of_lab_id = db.Column(db.ForeignKey('type_of_labs.id'))

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

    # @staticmethod
    # def get_lab_by_id(id, fields=None):
    #     # get the lab from the db
    #     lab = Lab.query.get(id)
    #     # if lab does not exist
    #     if not lab:
    #         return None
    #     lab = lab.to_client()
    #     # if request do not contain fields, return the data
    #     if not fields:
    #         return lab
    #     # if fields exist in the request, format the lab to have only the
    #     # fields requested by the user
    #     formatted_lab = Lab.format_labs_by_fields([lab], fields)[0]
    #     return formatted_lab

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

    @staticmethod
    def get_lab_by_id(id):
        return Lab.query.get(id)

    @staticmethod
    def get_lab_by_mnemonic(mnemonic):
        return Lab.query.filter_by(mnemonic=mnemonic).first()

    def get_id(self):
        return self.id

    def get_mnemonic(self):
        return self.mnemonic

    def get_name(self):
        return self.name

    def get_institute(self):
        return self.institute

    def get_discipline(self):
        return self.discipline

    def get_experiments(self):
        return self.experiments

    def get_integration_level(self):
        return self.integration_level.level

    def get_hosted_url(self):
        return self.hosted_url

    def get_repo_url(self):
        return self.repo_url

    def get_type(self):
        return self.type_of_lab

    def get_num_of_experiments(self):
        return len(self.experiments)

    def get_hosted_on(self):
        return self.hosted_on

    def is_web_2_compliant(self):
        return self.is_web_2_compliant

    def is_phase_2(self):
        return self.is_phase_2_lab

    def get_developers(self):
        return self.developers

    def get_technologies(self):
        return self.technologies

    @typecheck(name=Name)
    def set_name(self, name):
        self.name = name
        self.save()

    @typecheck(institute=Institute)
    def set_institute(self, institute):
        self.institute = institute
        self.save()

    @typecheck(discipline=Discipline)
    def set_discipline(self, discipline):
        self.discipline = discipline
        self.save()

    @typecheck(level=IntegrationLevel)
    def set_integration_level(self, level):
        self.integration_level = level
        self.save()

    @typecheck(url=URL)
    def set_hosted_url(self, url):
        self.hosted_url = url
        self.save()

    @typecheck(url=URL)
    def set_repo_url(self, url):
        self.repo_url = url
        self.save()

    @typecheck(type=TypeOfLab)
    def set_type_of_lab(self, type):
        self.type_of_lab = type
        self.save()

    @typecheck(platform=HostingPlatform)
    def set_hosted_on(self, platform):
        self.hosted_on = platform
        self.save()

    @typecheck(compliant=bool)
    def set_is_web_2_compliant(self, compliant):
        self.is_web_2_compliant = compliant
        self.save()

    @typecheck(phase2=bool)
    def set_is_phase_2_lab(self, phase2):
        self.is_phase_2_lab = phase2
        self.save()

    @typecheck(developer=Developer)
    def add_developer(self, developer):
        self.developers.append(developer)
        self.save()

    @typecheck(developer=Developer)
    def remove_developer(self, developer):
        if developer in self.developers:
            self.developers.remove(developer)
            self.save()

    @typecheck(technology=Technology)
    def add_technology(self, technology):
        self.technologies.append(technology)
        self.save()

    @typecheck(technology=Technology)
    def remove_technology(self, technology):
        if technology in self.technologies:
            self.technologies.remove(technology)
            self.save()

    @typecheck(experiment=Experiment)
    def add_experiment(self, experiment):
        self.experiments.append(experiment)
        self.save()

    @typecheck(experiment=Experiment)
    def remove_experiment(self, experiment):
        if experiment in self.experiments:
            self.experiments.remove(experiment)
            self.save()

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
            'technologies': self.technologies,
            'developers': self.developers,
            'type_of_lab': self.type_of_lab,
            'status': self.status,
            'is_web_2_compliant': self.is_web_2_compliant,
            'is_phase_2_lab': self.is_phase_2_lab,
            'remarks': self.remarks
        }
