from flask import Flask, request, jsonify
from db import db, Lab
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
	'mysql+oursql://root:root@localhost/vlabs_info'
db.init_app(app)
db.app = app

#Get all labs
@app.route('/labs', methods=['GET'])
def labs():
   if request.method == 'GET':
	fields = request.args.get('fields') or None
        print Lab.getAllLabs(fields)
        return "asdf"
	      

if __name__ == "__main__":
    app.run(debug=True)    
        
