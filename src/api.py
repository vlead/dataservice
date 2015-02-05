from flask import Blueprint, request, jsonify, json, abort
from db import Lab, Institute, Discipline, Technology


api = Blueprint('APIs', __name__)


#Get all labs
@api.route('/labs', methods=['GET', 'POST'])
def labs():
    if request.method == 'GET':
        fields = request.args.getlist('fields') or None
        return json.dumps(Lab.get_all(fields))

    if request.method == 'POST':
        if request.form:
            new_lab = Lab(**request.form.to_dict())
            new_lab.save()
            return jsonify(new_lab.to_client())


#Get all the labs of a specific discipline
@api.route('/labs/disciplines/<param>', methods =['GET'])
def labs_by_discipline(param):
    if request.method == 'GET':
        try:
            if param is None:
                abort(404)
            some = Discipline.query.filter_by(name=param).first()
            labs = Lab.query.filter_by(discipline_id=some.id).all()
            return json.dumps([i.to_client() for i in labs])
        except AttributeError:
            return "Enter valid discipline name."


#Get all the labs of a specific institute
@api.route('/labs/institutes/<param>', methods = ['GET'])
def labs_by_institute(param):
    if request.method == 'GET':
        try:
            if param is None:
                abort(404)
            some = Institute.query.filter_by(name=param).first()
            labs = Lab.query.filter_by(institute_id=some.id).all()
            return json.dumps([i.to_client() for i in labs])
        except AttributeError:
            return "Enter valid institute name."


#Get all institutes
@api.route('/institutes', methods=['GET', 'POST'])
def institutes():
    if request.method == 'GET':
        return json.dumps(Institute.get_all())

    if request.method == 'POST':
        if request.form:
            new_institute = Institute(**request.form.to_dict())
            new_institute.save()
            return jsonify(new_institute.to_client())


#Get all Disciplines
@api.route('/disciplines', methods=['GET', 'POST'])
def disciplines():
    if request.method == 'GET':
        return json.dumps(Discipline.get_all())

    if request.method == 'POST':
        if request.form:
            new_discipline = Discipline(**request.form.to_dict())
            new_discipline.save()
            return jsonify(new_discipline.to_client())

#Get all Technologies
@api.route('/technologies', methods=['GET', 'POST'])
def technologies():
    if request.method == 'GET':
        return json.dumps(Technology.get_all())

    if request.method == 'POST':
        if request.form:
            new_technology = Technology(**request.form.to_dict())
            new_technology.save()
            return jsonify(new_technology.to_client())


#Get a specific lab
@api.route('/labs/<int:id>', methods=['GET'])
def get_lab_by_id(id):
    if request.method == 'GET':
        lab = Lab.query.get(id)
        if lab is None:
            abort(404)

        return jsonify(lab.to_client())


#Get a parameter of a specific lab
@api.route('/labs/<int:id>/<param>', methods=['GET'])
def get_a_field(id, param):
    if request.method == 'GET':
        lab = Lab.query.get(id)
        if param is None:
            abort(404)
        field = lab.to_client()[param]
        print field
        resp = {}
        resp[param] = field
        return jsonify(resp)


