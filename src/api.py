from flask import Flask, request
from db import db, Lab

#api1 = Flask (__name__)
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
        return "sfsdf"        
        

if __name__ == "__main__":
    app.run(debug=True)    
         
        



