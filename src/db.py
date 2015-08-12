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

    old_lab_id = db.Column(db.String(32))
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128))

    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    discipline = db.relationship('Discipline')

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    institute = db.relationship('Institute')

    integration_level = db.Column(db.Integer, nullable=False)
    # integration_level_id = db.Column(db.ForeignKey('integration_levels.id'))
    # integration_level = db.relationship('IntegrationLevel')

    number_of_experiments = db.Column(db.Integer)

    is_src_avail = db.Column(db.Boolean)
    repo_url = db.Column(db.String(256))

    is_hosted = db.Column(db.Boolean)
    hosted_url = db.Column(db.String(256))
    hosted_on = db.Column(db.Enum('IIIT', 'AWS', 'BADAL', 'ELSE'))

    # hosted_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))
    # hosted_on = db.relationship('HostingPlatform')

    type_of_lab = db.Column(db.String(64))
    # type_of_lab_id = db.Column(db.ForeignKey('type_of_labs.id'))
    # type_of_lab = db.relationship('TypeOfLab')

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
            'name': self.name,
            'slug': self.slug,
            'institute': {
                'id': self.institute.id,
                'name': self.institute.name,
                'PIC': self.institute.PIC,
                'IIC': self.institute.IIC
            },
            'discipline': {
                'id': self.discipline.id,
                'name': self.discipline.name,
                'dnc': self.discipline.dnc
            },
            'integration_level': self.integration_level,
            'number_of_experiments': self.number_of_experiments,
            'is_src_avail': self.is_src_avail,
            'repo_url': self.repo_url,
            'is_hosted': self.is_hosted,
            'hosted_url': self.hosted_url,
            'hosted_on': self.hosted_on,
            'technologies': self.get_technologies(),
            'developers': self.get_developers(),
            'type_of_lab': self.type_of_lab,
            'remarks': self.remarks,
            'status': self.status,
            'old_lab_id': self.old_lab_id,
            'is_web_2_compliant': self.is_web_2_compliant,
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
            'institute': self.institute.to_client()
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


class TechnologyUsed(Entity):

    __tablename__ = 'technologies_used'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id'))
    experiment = db.relationship('Experiment')

    tech_id = db.Column(db.Integer, db.ForeignKey('technologies.id'))
    technology = db.relationship('Technology')

    server_side = db.Column(db.Boolean)
    client_side = db.Column(db.Boolean)


class Experiment(Entity):

    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True)

    # Our data set has really, really long experiment names and URLs!!
    name = db.Column(db.String(256))

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    content_url = db.Column(db.String(256))
    content_on = db.Column(db.Enum('CPE', 'ELSE', 'NA'))
    # content_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))
    # content_on = db.relationship('HostingPlatform')

    simulation_url = db.Column(db.String(256))
    simulation_on = db.Column(db.Enum('CPE', 'ELSE', 'NA'))
    # simulation_on_id = db.Column(db.ForeignKey('hosting_platforms.id'))
    # simulation_on = db.relationship('HostingPlatform')

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name,
            'content_url': self.content_url,
            'content_on': self.content_on,
            'simulation_url': self.simulation_url,
            'simulation_on': self.simulation_on,
            'lab': {
                'id': self.lab.id,
                'name': self.lab.name
            }
        }


class IntegrationLevel(Entity):
    __tablename__ = 'integration_levels'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)


class TypeOfLab(Entity):
    __tablename__ = 'type_of_labs'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)


class HostingPlatform(Entity):
    __tablename__ = 'hosting_platforms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)


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
