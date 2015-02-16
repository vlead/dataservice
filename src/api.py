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
        if not data:
            abort(400, 'Your data should be in JSON format')
        if "institute_id" not in data:
            abort(400, 'Provide institute_id')
        if "discipline_id" not in data:
            abort(400, 'Provide discipline_id')
            
        lab=Lab.query.get(data['institute_id'])
        if lab is None:
            abort(404,"Foreign_key constraint fails: Provide institute_id")
            
        dis = Discipline.query.get(data['discipline_id'])
        if dis is None:
            abort(404,"Foreign_key constraint fails: Provide discipline_id")
        try:
            new_lab = Lab(**data)
            new_lab.save()
            return jsonify(new_lab.to_client())

        except (TypeError,AttributeError):
            return jsonify(error="Wrong attribute found")
            
# Get all the labs of a specific discipline
@api.route('/disciplines/<int:id>/labs', methods=['GET'])
@api.route('/labs/disciplines/<int:id>', methods=['GET'])
def labs_by_discipline(id):
    if request.method == 'GET':
	if id is None:
            abort(404)

        labs = Lab.query.filter_by(discipline_id=id).all()
	if len(labs) == 0:
	    abort(404, 'Invalid Id')

        return json.dumps([i.to_client() for i in labs])

# Get all the labs of a specific institute
@api.route('/institutes/<int:id>/labs', methods=['GET'])
@api.route('/labs/institutes/<int:id>', methods=['GET'])
def labs_by_institute(id):
    if request.method == 'GET':
        if id is None:
            abort(404)

        labs = Lab.query.filter_by(institute_id=id).all()
	if len(labs) == 0:
	    abort(404, 'Invalid Id')

        return json.dumps([i.to_client() for i in labs])



# Get all the labs of a discipline of a specific institute
@api.route('/labs/institutes/<int:int_id>/disciplines/<int:disc_id>',
           methods=['GET'])
def labs_by_disc(int_id, disc_id):
        if request.method == 'GET':
            if int_id is None:
                abort(404)

            labs = Lab.query.filter_by(institute_id=int_id,
                                       discipline_id=disc_id).all()
            if len(labs) == 0:
		abort(404, 'Enter valid Id')

            return json.dumps([i.to_client() for i in labs])


# Get all the developer of a specific institute
@api.route('/institutes/<int:id>/developers', methods=['GET'])
def dev_by_inst(id):
        if request.method == 'GET':
            if id is None:
                abort(404)

            devlopers = Developer.query.filter_by(institute_id=id).all()
	    if len(devlopers) == 0:
		abort(404, 'No Developer found with this Id')

            return json.dumps([i.to_client() for i in devlopers])


# Get all institutes
@api.route('/institutes', methods=['GET', 'POST'])
def institutes():
    if request.method == 'GET':
        return json.dumps(Institute.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        try:
            new_institute = Institute(**data)
            new_institute.save()
            return jsonify(new_institute.to_client())

        except (TypeError,AttributeError):
            return "Error: Provide correct attribute name"
 
# update institutes by ID
@api.route('/institutes/<int:id>', methods=['PUT'])
def update_instt_by_id(id):
    if request.method == 'PUT':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        instt = Institute.query.get(id)
        if instt is None:
            abort(404)
        try:
            for key in data:
                instt.__setattr__(key, data[key])
                instt.save()
            return jsonify(instt.to_client())
        except (AttributeError,KeyError):
            return "Error: Provide correct attribute name"
                              
# Get all Disciplines
@api.route('/disciplines', methods=['GET', 'POST'])
def disciplines():
    if request.method == 'GET':
        return json.dumps(Discipline.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        try:
            new_discipline = Discipline(**data)
            new_discipline.save()
            return jsonify(new_discipline.to_client())

        except (TypeError,AttributeError):
            return "Error: Provide correct attribute name"
        
# update Disciplines by ID
@api.route('/disciplines/<int:id>', methods=['PUT'])
def update_disc_by_id(id):
    if request.method == 'PUT':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        disc = Discipline.query.get(id)
        if disc is None:
            abort(404)
        try:            
            for key in data:
                disc.__setattr__(key, data[key])
                disc.save()
            return jsonify(disc.to_client())
        except (KeyError,AttributeError):
            return "Invalid attribute found"
# Get all Technologies
@api.route('/technologies', methods=['GET', 'POST'])
def technologies():
    if request.method == 'GET':
        return json.dumps(Technology.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        try:
            new_technology = Technology(**data)
            new_technology.save()
            return jsonify(new_technology.to_client())

        except (TypeError,AttributeError):
            return "Error: Provide correct attribute name"
            
# Get all Developers
@api.route('/developers', methods=['GET', 'POST'])
def developers():
    if request.method == 'GET':
        return json.dumps(Developer.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        if 'institute_id' not in data:
            abort(400,"Provide institute_id")

        instt = Institute.query.get(data['institute_id'])
        
        try:
            new_develop = Developer(**data)
            new_develop.save()
            return jsonify(new_develop.to_client())

        except TypeError:
            return jsonify(error="Error: Provide correct attribute name")       
            
# updating Developers by ID
@api.route('/developers/<int:id>', methods=['PUT'])
def update_develop_by_id(id):
    if request.method == 'PUT':        
        develop = Developer.query.get(id)
        data = parse_request(request)
        if develop is None:
            abort(404,"No id found")
        if not data:
            abort(400, 'Your data should be in JSON format')
        try:
            
            for key in data:
                develop.__setattr__(key, data[key])
                develop.save()
            return jsonify(develop.to_client())
        except (AttributeError, TypeError):
            return "Provide correct attribute name"

# updating technologies by ID
@api.route('/technologies/<int:id>', methods=['PUT'])
def update_tech_by_id(id):
    if request.method == 'PUT':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        tech = Technology.query.get(id)
        #jsonify(request.form.to_dict())
        try:
            for key in data:
                tech.__setattr__(key, data[key])
                tech.save()
            return jsonify(tech.to_client())
        except (AttributeError,KeyError):
            return "Provide correct attribute name"

# Get a specific lab and its parameters 
# Example: /labs/1?fields=status&fields=discipline
@api.route('/labs/<int:id>', methods=['GET', 'PUT'])
def get_lab_by_id(id):
    if request.method == 'GET':
        lab = Lab.query.get(id)
        if lab is None:
            abort(404, 'Invalid Id')
	
	fields = request.args.getlist('fields') or None
	if fields is None:
            return jsonify(lab.to_client())

        fmttd_lab = {}  # formatted lab
        for field in fields:
	    try:
	        fmttd_lab[field] = lab.to_client()[field]
	    except KeyError:
	        raise Exception('Invalid field %s', field)
        return jsonify(fmttd_lab)
	
    if request.method == 'PUT':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        lab = Lab.query.get(id)
        #jsonify(request.form.to_dict())
        try:
            for key in data:
                lab.__setattr__(key, data[key])
                lab.save()
            return jsonify(lab.to_client())
        except (AttributeError,KeyError):
            return "Provide correct attribute name"

# Get labs info by searching with any of its parameters
@api.route('/search/labs', methods=['GET'])
def search():
    if request.method == 'GET':
        args = {}
        args = request.args.to_dict()
      #  print args
        if 'institute' in args:
            args['institute_id'] = \
                Institute.query.filter_by(name=args['institute']).first().id

            del(args['institute'])

        if 'discipline' in args:
            args['discipline_id'] = \
                Discipline.query.filter_by(name=args['discipline']).first().id

            del(args['discipline'])
       # print args

        labs = Lab.query.filter_by(**args).all()

        if not len(labs):
            abort(404, 'No labs found with your search query.')

        return json.dumps([lab.to_client() for lab in labs])

@api.route('/experiments/<int:id>', methods=['PUT'])
def update_exp_by_id(id):
    if request.method == 'PUT':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        exp = Experiment.query.get(id)
        if exp is None:
            abort(404)
        try:
            for key in request.form.to_dict():
                exp.__setattr__(key, request.form.to_dict()[key])
                exp.save()
            return jsonify(exp.to_client())
        except (AttributeError,KeyError):
            return "Provide correct attribute name"

# Get all the experiments of a specific lab
@api.route('/labs/<int:id>/experiments', methods=['GET'])
def get_all_experiments(id):
    if request.method == 'GET':
        lab = Lab.query.get(id)
        if lab is None:
            abort(404, 'Invalid Id')

        experiments = Experiment.query.filter_by(lab_id=lab.id).all()
	if len(experiments) == 0:
	    abort(404, 'No experiment found with this Id')

        return json.dumps([i.to_client() for i in experiments])


# Post all the experiments of a specific lab
@api.route('/experiments', methods=['POST'])
def post_exp():
    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        if 'lab_id' not in data:
            abort(400,'You need to provide lab_id')

        lab = Lab.query.get(data['lab_id'])

        if lab is None:
            abort(404, 'No lab exist with given lab_id')
        
        try:
            new_experiment = Experiment(**data)
            new_experiment.save()
            return jsonify(new_experiment.to_client())

        except (TypeError,AttributeError):
            return "Error: Provide correct attribute name"
