
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Lab(db.Model):

    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.String(32))
    name = db.Column(db.String(128))
    slug = db.Column(db.String(128))

    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'))
    discipline = db.relationship('Discipline')

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    institute = db.relationship('Institute')

    #developer_id = db.Column(db.Integer, db.ForeignKey('developers.id'))
    ##developer = db.Column(db.String(100), db.ForeignKey('developers.email_id'))
    #developer = db.relationship('Developer')

    repo_url = db.Column(db.String(256))
    hosted_url = db.Column(db.String(256))
    number_of_experiments = db.Column(db.Integer)

    integration_level = db.Column(db.Integer)
    type_of_lab = db.Column(db.String(64))
    remarks = db.Column(db.Text)
    status = db.Column(db.String(32))

    is_src_avail = db.Column(db.Boolean)
    is_deployed = db.Column(db.Boolean)
    is_content_avail = db.Column(db.Boolean)
    is_simulation = db.Column(db.Boolean)
    is_web_2_compliant = db.Column(db.Boolean)
    is_auto_hostable = db.Column(db.Boolean)
    is_phase_2_lab = db.Column(db.Boolean)

    @staticmethod
    def get_all(fields=None):

        labs = [i.to_client() for i in Lab.query.all()]
        #print fields
        if not fields:
            #return [i.to_client() for i in Lab.query.all()]
            return labs

        fmttd_labs = []  # all labs
        for lab in labs:
            fmttd_lab = {}  # formatted lab
            for field in fields:
                try:
                    fmttd_lab[field] = lab[field]
                except KeyError:
                    raise Exception('Invalid field %s', field)

                #print fmttd_lab
                fmttd_labs.append(fmttd_lab)

        return fmttd_labs

    def __init__(self, **kwargs):
        super(Lab, self).__init__(**kwargs)
        #TODO: see if we can find a better way to type convert these fields to
        #boolean
        self.is_src_avail = True if self.is_src_avail == "True" else False
        self.is_phase_2_lab = True if self.is_phase_2_lab == "True" else False
        self.is_deployed = True if self.is_deployed == "True" else False
        self.is_auto_hostable = True if self.is_auto_hostable == "True" else False
        self.is_content_avail = True if self.is_content_avail == "True" else False
        self.is_simulation = True if self.is_simulation == "True" else False
        self.is_web_2_compliant = True if self.is_web_2_compliant == "True" else False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_client(self):
        return {
            'id': self.id,
            'lab_id': self.lab_id,
            'name': self.name,
            'slug': self.slug,
            'institute': {
                'id': self.institute.id,
                'name': self.institute.name,
                'coordinator': self.institute.coordinators,
                'integration_coordinator': self.institute.integration_coordinators
            },
            'discipline': {
                'id': self.discipline.id,
                'name': self.discipline.name,
                'dnc': self.discipline.dnc
            },
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
            'is_simulation': self.is_simulation,
            'is_web_2_compliant': self.is_web_2_compliant,
            'is_auto_hostable': self.is_auto_hostable,
            'is_phase_2_lab': self.is_phase_2_lab
        }


class Institute(db.Model):

    __tablename__ = 'institutes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    coordinators = db.Column(db.String(128))
    integration_coordinators = db.Column(db.String(128))

    def to_client(self):
        return {
            'name': self.name,
            'coordinator': self.coordinators,
            'integration_coordinator': self.integration_coordinators
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in Institute.query.all()]

    def save(self):
        db.session.add(self)
        db.session.commit()


class Discipline(db.Model):

    __tablename__ = 'disciplines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    dnc = db.Column(db.String(64))

    def to_client(self):
        return {
            'name': self.name,
            'dnc': self.dnc
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in Discipline.query.all()]

    def save(self):
        db.session.add(self)
        db.session.commit()


class Developer(db.Model):

    __tablename__ = 'developers'

    id = db.Column(db.Integer, primary_key=True)

    email_id = db.Column(db.String(128))
    name = db.Column(db.String(64))

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    institute = db.relationship('Institute')

    def to_client(self):
     return {
            'id':self.id,
            'email_id': self.email_id,
            'name': self.name,
            'institute_id':self.institute_id
        }

    @staticmethod
    def get_all():
        return [i.to_client() for i in Developer.query.all()]

    def save(self):
        db.session.add(self)
        db.session.commit()

class DeveloperEngaged(db.Model):

    __tablename__ = 'developers_engaged'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    developer_id = db.Column(db.Integer, db.ForeignKey('developers.id'))
    lab = db.relationship('Developer')


class Technology(db.Model):

    __tablename__ = 'technologies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    foss = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        super(Technology, self).__init__(**kwargs)
        self.foss = True if self.foss == "True" else False

    @staticmethod
    def get_all():
        return [i.to_client() for i in Technology.query.all()]

    def to_client(self):
        return {
            'name': self.name,
            'foss': self.foss
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class TechnologyUsed(db.Model):

    __tablename__ = 'technologies_used'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship('Lab')

    tech_id = db.Column(db.Integer, db.ForeignKey('technologies.id'))
    technology = db.relationship('Technology')

    server_side = db.Column(db.Boolean)
    client_side = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        super(TechnologyUsed, self).__init__(**kwargs)
        self.server_side = True if self.server_side == "True" else False
        self.client_side = True if self.client_side == "True" else False

class Experiment(db.Model):

  __tablename__ = 'experiments'

  id = db.Column(db.Integer, primary_key=True)

  lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
  lab = db.relationship('Lab')

  name = db.Column(db.String(64))
  content_url = db.Column(db.String(150))
  simulation_url = db.Column(db.String(150))

  def to_client(self):
          return {
                        'id': self.id,
                        'name':self.name,
                        'content_url':self.content_url,
                        'simulation_url':self.simulation_url,
                        'lab': {
                                          'id': self.lab.id,
                               }
                }
  def save(self):
            db.session.add(self)
            db.session.commit()

