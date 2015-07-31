# -*- coding: utf-8 -*-


from flask import Blueprint, request, jsonify, abort, current_app

from db import *
from utils import parse_request, jsonify_list


api = Blueprint('APIs', __name__)


# Get all labs
@api.route('/labs', methods=['GET', 'POST'])
def labs():
    if request.method == 'GET':
        fields = request.args.getlist('fields') or None
        try:
            current_app.logger.debug(jsonify_list(Lab.get_all(fields)).data)
            return jsonify_list(Lab.get_all(fields))
        except Exception:
            abort(404, 'Invalid field attribute')

    if request.method == 'POST':
        data = parse_request(request)

        if not data:
            abort(400, 'Your data should be in JSON format')

        if 'institute_id' not in data:
            abort(400, 'Provide institute_id')

        if 'discipline_id' not in data:
            abort(400, 'Provide discipline_id')

        instt = Institute.query.get(data['institute_id'])

        if instt is None:
            abort(404, 'Foreign_key constraint fails: Provide institute_id')

        dis = Discipline.query.get(data['discipline_id'])

        if dis is None:
            abort(404, 'Foreign_key constraint fails: Provide discipline_id')
        try:
            new_lab = Lab(**data)
            new_lab.save()
            return jsonify(new_lab.to_client())

        except (TypeError, AttributeError), e:
            current_app.logger.error("Error while saving lab data: %s" % e)
            abort(400, 'Invalid attributes in request data')


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

        return jsonify_list([i.to_client() for i in labs])


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

        return jsonify_list([i.to_client() for i in labs])


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

            return jsonify_list([i.to_client() for i in labs])


# Get all the developer of a specific institute
@api.route('/institutes/<int:id>/developers', methods=['GET'])
def dev_by_inst(id):
        if request.method == 'GET':
            if id is None:
                abort(404)

            devlopers = Developer.query.filter_by(institute_id=id).all()
            if len(devlopers) == 0:
                abort(404, 'No Developer found with this Id')

            return jsonify_list([i.to_client() for i in devlopers])


# Get all institutes
@api.route('/institutes', methods=['GET', 'POST'])
def institutes():
    if request.method == 'GET':
        return jsonify_list(Institute.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        try:
            new_institute = Institute(**data)
            new_institute.save()
            return jsonify(new_institute.to_client())

        except (TypeError, AttributeError), e:
            current_app.logger.error("Error while saving institute data: %s" %
                                     e)
            # return 'Error: Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')


# update institutes by ID
@api.route('/institutes/<int:id>', methods=['PUT'])
def update_instt_by_id(id):
    if request.method == 'PUT':

        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        instt = Institute.query.get(id)
        if instt is None:
            abort(404, 'No institute with id: %s found' % str(id))

        try:
            instt.update(**data)
        except (AttributeError, KeyError), e:
            current_app.logger.error("Error while saving institute data: %s" %
                                     e)
            # return 'Error: Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')

        return jsonify(instt.to_client())


# Get all Disciplines
@api.route('/disciplines', methods=['GET', 'POST'])
def disciplines():
    if request.method == 'GET':
        return jsonify_list(Discipline.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        try:
            new_discipline = Discipline(**data)
            new_discipline.save()
            return jsonify(new_discipline.to_client())

        except (TypeError, AttributeError), e:
            current_app.logger.error("Error while saving discipline data: %s" %
                                     e)
            # return 'Error: Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')


# update Disciplines by ID
@api.route('/disciplines/<int:id>', methods=['PUT'])
def update_disc_by_id(id):
    if request.method == 'PUT':

        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        disc = Discipline.query.get(id)
        if disc is None:
            abort(404, 'No discipline with id: %s found' % str(id))

        try:
            disc.update(**data)
        except (KeyError, AttributeError), e:
            current_app.logger.error("Error while saving discipline data: %s" %
                                     e)
            # return 'Invalid attribute found'
            abort(400, 'Invalid attributes in request data')

        return jsonify(disc.to_client())


# Get all Technologies
@api.route('/technologies', methods=['GET', 'POST'])
def technologies():
    if request.method == 'GET':
        return jsonify_list(Technology.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')
        try:
            new_technology = Technology(**data)
            new_technology.save()
            return jsonify(new_technology.to_client())

        except (TypeError, AttributeError), e:
            current_app.logger.error("Error while saving technology data: %s" %
                                     e)
            # return 'Error: Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')


# Get all Developers
@api.route('/developers', methods=['GET', 'POST'])
def developers():
    if request.method == 'GET':
        return jsonify_list(Developer.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        if 'institute_id' not in data:
            abort(400, 'Provide institute_id')

        # instt = Institute.query.get(data['institute_id'])

        try:
            new_develop = Developer(**data)
            new_develop.save()
            return jsonify(new_develop.to_client())

        except TypeError, e:
            current_app.logger.error("Error while saving developer data: %s" %
                                     e)
            # return jsonify(error='Error: Provide correct attribute name')
            abort(400, 'Invalid attributes in request data')


# updating Developers by ID
@api.route('/developers/<int:id>', methods=['PUT'])
def update_develop_by_id(id):
    if request.method == 'PUT':

        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        develop = Developer.query.get(id)
        if develop is None:
            abort(404, 'No developer with id: %s found' % str(id))

        try:
            develop.update(**data)
        except (AttributeError, TypeError), e:
            current_app.logger.error("Error while saving developer data: %s" %
                                     e)
            # return 'Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')

        return jsonify(develop.to_client())


# updating technologies by ID
@api.route('/technologies/<int:id>', methods=['PUT'])
def update_tech_by_id(id):
    if request.method == 'PUT':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        tech = Technology.query.get(id)
        if not tech:
            abort(404, 'No such technology exist')

        try:
            tech.update(**data)
        except (AttributeError, KeyError), e:
            current_app.logger.error("Error while saving technology data: %s" %
                                     e)
            # return 'Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')

        return jsonify(tech.to_client())


# Get a specific lab and its parameters
# Example: /labs/1?fields=status&fields=discipline
@api.route('/labs/<int:id>', methods=['GET', 'PUT'])
def get_lab_by_id(id):
    if request.method == 'GET':
        fields = request.args.getlist('fields') or None

        try:
            lab_dict = Lab.get_specific_lab(id, fields)
        except Exception:
            abort(400, 'Invalid field attribute')

        if lab_dict is None:
            abort(404, 'Invalid id')

        return jsonify(lab_dict)

    if request.method == 'PUT':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        lab = Lab.query.get(id)
        if not lab:
            abort(404, 'No lab with id: %s exist' % str(id))

        try:
            lab.update(**data)
        except (AttributeError, KeyError), e:
            current_app.logger.error("Error while saving lab data: %s" % e)
            # return 'Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')

        return jsonify(lab.to_client())


# Get labs info by searching with any of its parameters
@api.route('/search/labs', methods=['GET'])
def search():
    if request.method == 'GET':
        args = {}
        args = request.args.to_dict()
        current_app.logger.debug("args received for /search request: %s" % args)
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
            abort(404, 'No labs found with your search query')

        return jsonify_list([lab.to_client() for lab in labs])


@api.route('/experiments/<int:id>', methods=['PUT'])
def update_exp_by_id(id):
    if request.method == 'PUT':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        exp = Experiment.query.get(id)
        if exp is None:
            abort(404, 'No such experiment')

        try:
            exp.update(**data)
        except (AttributeError, KeyError):
            # return 'Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')

        return jsonify(exp.to_client())


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

        return jsonify_list([i.to_client() for i in experiments])


# Post all the experiments of a specific lab
@api.route('/experiments', methods=['POST'])
def post_exp():
    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        if 'lab_id' not in data:
            abort(400, 'You need to provide lab_id')

        lab = Lab.query.get(data['lab_id'])

        if lab is None:
            abort(404, 'No lab exist with given lab_id')

        try:
            new_experiment = Experiment(**data)
            new_experiment.save()
            return jsonify(new_experiment.to_client())

        except (TypeError, AttributeError), e:
            current_app.logger.error("Error saving experiment data: %s" % e)
            # return 'Error: Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')


# Get all system details of a lab
@api.route('/labsysteminfo', methods=['GET', 'POST'])
def get_labsysteminfo():
    if request.method == 'GET':
        return jsonify_list(LabSystemInfo.get_all())

    if request.method == 'POST':
        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        if 'lab_id' not in data:
            abort(400, 'You need to provide lab_id')

        lab = Lab.query.get(data['lab_id'])

        if lab is None:
            abort(404, 'No lab exist with given lab_id')

        try:
            new_system_info = LabSystemInfo(**data)
            new_system_info.save()
            return jsonify(new_system_info.to_client())

        except (TypeError, AttributeError), e:
            current_app.logger.error("Error saving labs system info data: %s" %
                                     e)
            # return 'Error: Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')


# updating LabSystemInfo by ID
@api.route('/labsysteminfo/<int:id>', methods=['PUT'])
def update_labsysteminfo_by_id(id):
    if request.method == 'PUT':

        data = parse_request(request)
        if not data:
            abort(400, 'Your data should be in JSON format')

        labsysteminfo = LabSystemInfo.query.get(id)
        if labsysteminfo is None:
            abort(404, 'No id found')

        try:
            labsysteminfo.update(**data)
        except (AttributeError, TypeError), e:
            current_app.logger.error("Error saving labs system info data: %s" %
                                     e)
            # return 'Provide correct attribute name'
            abort(400, 'Invalid attributes in request data')

        return jsonify(labsysteminfo.to_client())
