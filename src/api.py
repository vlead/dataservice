from flask import Blueprint, request, jsonify, json, abort,current_app
from db import db, Lab, Institute, Discipline, Technology


api = Blueprint('APIs', __name__)


#Get all labs
@api.route('/labs', methods=['GET', 'POST'])
def labs():
    if request.method == 'GET':
	fields = request.args.get('fields') or None
	return json.dumps(Lab.getAllLabs(fields))

    if request.method == 'POST':
        if request.form:
            new_lab = Lab(**request.form.to_dict()) 
            new_lab.save()
            return jsonify(new_lab.to_client())
        

#Get all institutes
@api.route('/institutes', methods=['GET','POST'])
def institutes():
    if request.method == 'GET':
      fields = request.args.get('fields') or None
        #print Institute.getAllInstitutes(fields)
      return json.dumps(Institute.getAllInstitutes(fields))
    
    if request.method == 'POST':
        if request.form:
            new_institute = Institute(**request.form.to_dict())
            new_institute.save()
            return jsonify(new_institute.to_client())


#Get all Disciplines
@api.route('/disciplines', methods=['GET', 'POST'])
def disciplines():
    if request.method == 'GET':
        fields = request.args.get('fields') or None
        return json.dumps(Discipline.getAllDisciplines(fields))

    if request.method == 'POST':
        if request.form:
            new_discipline = Discipline(**request.form.to_dict())
            new_discipline.save()
            return jsonify(new_discipline.to_client())

#Get all Technologies
@api.route('/technologies', methods=['GET','POST'])
def technologies():
    if request.method == 'GET':
        fields = request.args.get('fields') or None
        return json.dumps(Technology.getAllTechnologies(fields))

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

