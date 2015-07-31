# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()


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


class Lab(Entity):

    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.String(32))
    name = db.Column(db.String(128))
    slug = db.Column(db.String(128))

    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    discipline = db.relationship('Discipline')

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    institute = db.relationship('Institute')

    repo_url = db.Column(db.String(256))
    hosted_url = db.Column(db.String(256))
    number_of_experiments = db.Column(db.Integer)

    integration_level = db.Column(db.Integer)
    # TODO : add a available_types attribute which is a set of available
    # type of labs; the application selects and validates the type_of_lab from
    # this set and stores it in the db
    type_of_lab = db.Column(db.String(64))
    remarks = db.Column(db.Text)
    status = db.Column(db.String(32))

    is_src_avail = db.Column(db.Boolean)
    is_deployed = db.Column(db.Boolean)
    is_content_avail = db.Column(db.Boolean)
    is_simulation_avail = db.Column(db.Boolean)
    is_web_2_compliant = db.Column(db.Boolean)
    is_auto_hostable = db.Column(db.Boolean)
    is_phase_2_lab = db.Column(db.Boolean)

    @staticmethod
    def get_all(fields=None):

        # get all labs from db
        labs = [i.to_client() for i in Lab.query.all()]
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

    def get_developers(self):
        devs = DeveloperEngaged.query.filter_by(lab_id=self.id).all()
        # print devs
        return [d.developer.to_client() for d in devs]

    def get_technologies(self):
        techs = TechnologyUsed.query.filter_by(lab_id=self.id).all()
        return [t.technology.to_client() for t in techs]

    def to_client(self):
        return {
            'id': self.id,
            'lab_id': self.lab_id,
            'name': self.name,
            'slug': self.slug,
            'institute': {
                'id': self.institute.id,
                'name': self.institute.name,
                'PIC': self.institute.PIC,
                'IIC':
                self.institute.IIC
            },
            'discipline': {
                'id': self.discipline.id,
                'name': self.discipline.name,
                'dnc': self.discipline.dnc
            },
            'developers': self.get_developers(),
            'technologies': self.get_technologies(),
            'repo_url': self.repo_url,
            'hosted_url': self.hosted_url,
            'number_of_experiments': self.number_of_experiments,
            'integration_level': self.integration_level,
            'type_of_lab': self.type_of_lab,
            'remarks': self.remarks,
            'status': self.status,
            'is_src_avail': self.is_src_avail,
            'is_content_avail': self.is_content_avail,
            'is_deployed': self.is_deployed,
            'is_simulation_avail': self.is_simulation_avail,
            'is_web_2_compliant': self.is_web_2_compliant,
            'is_auto_hostable': self.is_auto_hostable,
            'is_phase_2_lab': self.is_phase_2_lab
        }


class Institute(Entity):

    __tablename__ = 'institutes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    PIC = db.Column(db.String(128))
    IIC = db.Column(db.String(128))

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'PIC': self.PIC,
            'IIC': self.IIC
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in Institute.query.all()]


class Discipline(Entity):

    __tablename__ = 'disciplines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    dnc = db.Column(db.String(64))

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'dnc': self.dnc
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in Discipline.query.all()]


class Developer(Entity):

    __tablename__ = 'developers'

    id = db.Column(db.Integer, primary_key=True)

    email_id = db.Column(db.String(128))
    name = db.Column(db.String(64))

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    institute = db.relationship('Institute')

    def to_client(self):
        return {
            'id': self.id,
            'email_id': self.email_id,
            'name': self.name,
            'institute_id': self.institute_id
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in Developer.query.all()]


class DeveloperEngaged(Entity):

    __tablename__ = 'developers_engaged'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    developer_id = db.Column(db.Integer, db.ForeignKey('developers.id'))
    developer = db.relationship('Developer')


class Technology(Entity):

    __tablename__ = 'technologies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    foss = db.Column(db.Boolean)

    @staticmethod
    def get_all():
        return [i.to_client() for i in Technology.query.all()]

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'foss': self.foss
        }


class TechnologyUsed(Entity):

    __tablename__ = 'technologies_used'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    tech_id = db.Column(db.Integer, db.ForeignKey('technologies.id'))
    technology = db.relationship('Technology')

    server_side = db.Column(db.Boolean)
    client_side = db.Column(db.Boolean)


class Experiment(Entity):

    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    # Our data set has really, really long experiment names and URLs!!
    name = db.Column(db.String(256))
    content_url = db.Column(db.String(256))
    simulation_url = db.Column(db.String(256))

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'content_url': self.content_url,
            'simulation_url': self.simulation_url,
            'lab': {
                'id': self.lab.id,
            }
        }


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
