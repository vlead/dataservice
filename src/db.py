from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Lab(db.Model):

    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)

    lab_id = db.Column(db.String(45))
    lab_name = db.Column(db.String(100))

    discipline_id = db.Column(db.String(100),
                              db.ForeignKey('disciplines.discipline_name'))
    discipline = db.relationship('Discipline')

    institute_id = db.Column(db.Integer, db.ForeignKey('institutes.id'))
    institute = db.relationship('Institute')

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
    phase_2_lab = db.Column(db.String(45))

    def to_client(self):
        return {
            'lab_id': self.lab_id,
            'lab_name': self.lab_name,
            'institute': {
                'institute_name': self.institute.institute_name,
                'institute_coordinator': self.institute.institute_coordinators,
                'institute_integration_coordinator': self.institute.institute_integration_coordinators
            },
            'discipline': {
                'discipline_name': self.discipline.discipline_name,
                'dnc': self.discipline.dnc
            },
            'developer': {
                'name': self.developer_obj.developer_name,
                'email': self.developer_obj.email_id
            },
            'repo_url': self.repo_url,

            'sources_available': self.sources_available,
            'hosted_url': self.hosted_url,
            'lab_deployed': self.lab_deployed,
            'number_of_experiments': self.number_of_experiments,
            'content': self.content,
            'simulation': self.simulation,
            'web_2_compliance': self.web_2_compliance,
            'type_of_lab': self.type_of_lab,
            'auto_hostable': self.auto_hostable,
            'remarks': self.remarks,
            'integration_level': self.integration_level,
            'status': self.status,
            'phase_2_lab': self.phase_2_lab
        }

    @staticmethod
    def getAllLabs(fields):

        print fields
        if not fields:
            return [i.to_client() for i in Lab.query.all()]
            #return map(lambda x: x.to_client(), Lab.query.all())

        labs = []  # all labs
        for lab in Lab.query.all():
            fmttd_lab = {}  # formatted lab
            for field in fields:
                try:
                    fmttd_lab[field] = lab[field]
                except KeyError:
                    raise Exception('Invalid field %s', field)

                labs.append(fmttd_lab)
        return labs


class Institute(db.Model):

    __tablename__ = 'institutes'

    id = db.Column(db.Integer, primary_key=True)
    institute_name = db.Column(db.String(45))
    institute_coordinators = db.Column(db.String(100))
    institute_integration_coordinators = db.Column(db.String(100))

    def to_client(self):
        return {
            'institute_name': self.institute_name,
            'institute_coordinator': self.institute_coordinators,
            'institute_integration_coordinator': self.institute_integration_coordinators
        }

    @staticmethod
    def getAllInstitutes(fields):
        for i in Institute.query.all():
            return [i.to_client() for i in Institute.query.all()]


class Discipline(db.Model):

    __tablename__ = 'disciplines'

    id = db.Column(db.Integer)
    discipline_name = db.Column(db.String(100), primary_key=True)
    dnc = db.Column(db.String(50))

    def to_client(self):
        return {
            'discipline_name': self.discipline_name,
            'dnc': self.dnc
        }

    @staticmethod
    def getAllDisciplines(fields):
        for i in Discipline.query.all():
            return [i.to_client() for i in Discipline.query.all()]


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

    def to_client(self):
        return {
            'technology_name': self.technology_name,
            'foss': self.foss
        }

    @staticmethod
    def getAllTechnologies(fields):
        for i in Technology.query.all():
            return [i.to_client() for i in Technology.query.all()]


class TechnologyUsed(db.Model):

    __tablename__ = 'technologies_used'

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    tech_id = db.Column(db.Integer, db.ForeignKey('technologies.id'))
    technology_name = db.Column(db.String(100))
    foss = db.Column(db.String(100))
