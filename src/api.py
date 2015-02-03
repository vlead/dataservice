from flask import Blueprint, request, jsonify, json, abort,current_app
from db import db, Lab, Institute, Discipline, Technology


api = Blueprint('APIs', __name__)


#Get all labs
@api.route('/labs', methods=['GET', 'POST'])
def labs():
    if request.method == 'GET':
	    fields = request.args.get('fields') or None
	    #print Lab.getAllLabs(fields)[0]
	    #return jsonify(labs=Lab.getAllLabs(fields))
	    return json.dumps(Lab.getAllLabs(fields))
    if request.method == 'POST':
        if request.form:
            data ={}
            for key in request.form:
                data[key] = request.form.get(key)
            
            print data
            print type(data)
        new_lab = Lab(**data) 
        #new_lab.insert(**data)
        #print new_lab
        new_lab.save()
        return jsonify(new_lab.to_client())
        
         #else:
         #  abort(400)
	#dataDict = json.dumps(data)
  #print dataDictel

#Get all institutes
@api.route('/institutes', methods=['GET'])
def institutes():
    if request.method == 'GET':
        fields = request.args.get('fields') or None
        #print Institute.getAllInstitutes(fields)
        return json.dumps(Institute.getAllInstitutes(fields))


#Get all Disciplines
@api.route('/disciplines', methods=['GET'])
def disciplines():
    if request.method == 'GET':
        fields = request.args.get('fields') or None
        return json.dumps(Discipline.getAllDisciplines(fields))


#Get all Technologies
@api.route('/technologies', methods=['GET'])
def technologies():
    if request.method == 'GET':
        fields = request.args.get('fields') or None
        return json.dumps(Technology.getAllTechnologies(fields))


#get a specific lab
@api.route('/labs/<int:id>', methods=['GET'])
def get_lab_by_id(id):
    if request.method == 'GET':
        field = Lab.query.get(id)
        if field is None:
            abort(404)
        current_app.logger.debug('get_lab_by_id: %s', field)
        return jsonify(field.to_client())
