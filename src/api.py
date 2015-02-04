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

#get a specific lab
@api.route('/labs/<int:id>', methods=['GET'])
def get_lab_by_id(id):
    if request.method == 'GET':
        field = Lab.query.get(id)
        if field is None:
            abort(404)
        current_app.logger.debug('get_lab_by_id: %s', field)
        return jsonify(field.to_client())
