# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, json, abort
from db import Lab, Institute, Discipline, Technology, Developer, Experiment

from utils import parse_request

api = Blueprint('APIs', __name__)


# Get all labs
@api.route('/labs', methods=['GET', 'POST'])
def labs():
    if request.method == 'GET':
        fields = request.args.getlist('fields') or None
        return json.dumps(Lab.get_all(fields))

    if request.method == 'POST':
        data = parse_request(request)
        print data
        if not data:
            abort(400, 'Your data should be in JSON format')

        new_lab = Lab(**data)
        print new_lab
        new_lab.save()
        return jsonify(new_lab.to_client())


# Get all the labs of a specific discipline
@api.route('/labs/disciplines/<disc_name>', methods=['GET'])
def labs_by_discipline(disc_name):
    if request.method == 'GET':
        try:
            if disc_name is None:
                abort(404)
            field = Discipline.query.filter_by(name=disc_name).first()
            labs = Lab.query.filter_by(discipline_id=field.id).all()
            return json.dumps([i.to_client() for i in labs])

        except AttributeError:
            return "Enter valid discipline name."


# Get all the labs of a specific institute
@api.route('/labs/institutes/<inst_name>', methods=['GET'])
def labs_by_institute(inst_name):
    if request.method == 'GET':
        try:
            if inst_name is None:
                abort(404)
            field = Institute.query.filter_by(name=inst_name).first()
            labs = Lab.query.filter_by(institute_id=field.id).all()
            return json.dumps([i.to_client() for i in labs])

        except AttributeError:
            return "Enter valid institute name."


# Get all the labs of all disciplines of a specific institute
@api.route('/labs/institutes/<inst_name>/disciplines/<disc_name>',
           methods=['GET'])
def labs_by_disc(inst_name, disc_name):
    try:
        if request.method == 'GET':
            if inst_name is None:
                abort(404)
            disc = Discipline.query.filter_by(name=disc_name).first()
            instt = Institute.query.filter_by(name=inst_name).first()
            labs = Lab.query.filter_by(institute_id=instt.id,
                                       discipline_id=disc.id).all()
            return json.dumps([i.to_client() for i in labs])

    except AttributeError:
        return "Please enter valid search"


# Get all the developer of a specific institute
@api.route('/institutes/<inst_name>/developers', methods=['GET'])
def dev_by_inst(inst_name):
    try:
        if request.method == 'GET':
            if inst_name is None:
                abort(404)
            instt = Institute.query.filter_by(name=inst_name).first()
            devlopers = Developer.query.filter_by(institute_id=instt.id).all()
            return json.dumps([i.to_client() for i in devlopers])

    except AttributeError:
        return "Please enter valid institute name"


# Get all institutes
@api.route('/institutes', methods=['GET', 'POST'])
def institutes():
    if request.method == 'GET':
        return json.dumps(Institute.get_all())

    if request.method == 'POST':
        if request.form:
            new_institute = Institute(**request.form.to_dict())
            new_institute.save()
            return jsonify(new_institute.to_client())


# update institutes by ID
@api.route('/institutes/<int:id>', methods=['PUT'])
def update_instt_by_id(id):
    if request.method == 'PUT':
        instt = Institute.query.get(id)
        for key in request.form.to_dict():
            instt.__setattr__(key, request.form.to_dict()[key])
            print instt.to_client()
            instt.save()
            return jsonify(instt.to_client())


# Get all Disciplines
@api.route('/disciplines', methods=['GET', 'POST'])
def disciplines():
    if request.method == 'GET':
        return json.dumps(Discipline.get_all())

    if request.method == 'POST':
        if request.form:
            new_discipline = Discipline(**request.form.to_dict())
            new_discipline.save()
            return jsonify(new_discipline.to_client())


# update Disciplines by ID
@api.route('/disciplines/<int:id>', methods=['PUT'])
def update_disc_by_id(id):
    if request.method == 'PUT':
        disc = Discipline.query.get(id)
        for key in request.form.to_dict():
            disc.__setattr__(key, request.form.to_dict()[key])
            print disc.to_client()
            disc.save()
            return jsonify(disc.to_client())


# Get all Technologies
@api.route('/technologies', methods=['GET', 'POST'])
def technologies():
    if request.method == 'GET':
        return json.dumps(Technology.get_all())

    if request.method == 'POST':
        if request.form:
            new_technology = Technology(**request.form.to_dict())
            new_technology.save()
            return jsonify(new_technology.to_client())


# Get all Developers
@api.route('/developers', methods=['GET', 'POST'])
def developers():
    if request.method == 'GET':
        return json.dumps(Developer.get_all())

    if request.method == 'POST':
        if request.form:
            new_technology = Developer(**request.form.to_dict())
            new_technology.save()
            return jsonify(new_technology.to_client())


# updating Developers by ID
@api.route('/developers/<int:id>', methods=['PUT'])
def update_develop_by_id(id):
    if request.method == 'PUT':
        develop = Developer.query.get(id)
        jsonify(request.form.to_dict())
        for key in request.form.to_dict():
            develop.__setattr__(key, request.form.to_dict()[key])
        print develop.to_client()
        develop.save()
        return jsonify(develop.to_client())


# updating technologies by ID
@api.route('/technologies/<int:id>', methods=['PUT'])
def update_tech_by_id(id):
    if request.method == 'PUT':
        tech = Technology.query.get(id)
        jsonify(request.form.to_dict())
        for key in request.form.to_dict():
            tech.__setattr__(key, request.form.to_dict()[key])
            print tech.to_client()
            tech.save()
            return jsonify(tech.to_client())


# Get a specific lab
@api.route('/labs/<int:id>', methods=['GET', 'PUT'])
def get_lab_by_id(id):
    if request.method == 'GET':
        lab = Lab.query.get(id)
        if lab is None:
            abort(404)

        return jsonify(lab.to_client())

    if request.method == 'PUT':
        lab = Lab.query.get(id)
        jsonify(request.form.to_dict())
        for key in request.form.to_dict():
            lab.__setattr__(key, request.form.to_dict()[key])
            print lab.to_client()
            lab.save()
            return jsonify(lab.to_client())


# Get a parameter of a specific lab
@api.route('/labs/<int:id>/<param>', methods=['GET'])
def get_a_field(id, param):
    try:
        if request.method == 'GET':
            lab = Lab.query.get(id)
            if param is None:
                abort(404)

            field = lab.to_client()[param]
            print field
            resp = {}
            resp[param] = field
            return jsonify(resp)

    except (KeyError, AttributeError):
        return "Please enter valid attribute"


# Get labs info by searching with any of its parameters
@api.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        args = {}
        args = request.args.to_dict()
        print args
        if 'institute' in args:
            args['institute_id'] = \
                Institute.query.filter_by(name=args['institute']).first().id

            del(args['institute'])

        if 'discipline' in args:
            args['discipline_id'] = \
                Discipline.query.filter_by(name=args['discipline']).first().id

            del(args['discipline'])
        print args

        labs = Lab.query.filter_by(**args).all()

        if not len(labs):
            abort(404, 'No labs found with your search query.')

        return json.dumps([lab.to_client() for lab in labs])


@api.route('/experiments/<int:id>', methods=['PUT'])
def update_exp_by_id(id):
    if request.method == 'PUT':
        exp = Experiment.query.get(id)

        for key in request.form.to_dict():
            exp.__setattr__(key, request.form.to_dict()[key])
            print exp.to_client()
            exp.save()
            return jsonify(exp.to_client())


# Get all the experiments of a specific lab
@api.route('/labs/<int:id>/experiments', methods=['GET'])
def get_all_experiments(id):
    if request.method == 'GET':
        try:
            if id is None:
                abort(404)

            lab = Lab.query.get(id)
            experiments = Experiment.query.filter_by(lab_id=lab.id).all()
            return json.dumps([i.to_client() for i in experiments])

        except AttributeError:
            return "Enter valid lab id"


# Post all the experiments of a specific lab
@api.route('/experiments', methods=['POST'])
def post_exp():
    if request.method == 'POST':
        try:
            lab = Lab.query.get(int(request.form['lab_id']))
            if int(lab.id) is int(request.form['lab_id']):
                new_experiment = Experiment(**request.form.to_dict())
                new_experiment.save()
                return jsonify(new_experiment.to_client())

        except AttributeError:

            return "Enter valid lab_id"
