#!/usr/bin/python
import json
import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","root","vlabs_database" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# loads config.json, to retrieve adapter_name and adapter_port

try:
    config_spec = json.loads(open("./config.json").read())
except IOError as e:
    print ("unable to load config.json. Exception: " + str(e))
    raise e
except  Exception as e:
    print("unable to parse config.json. Exception: " + str(e))
    raise e
adapter_name = config_spec['ADAPTER_NAME']
adapter_port = config_spec['ADAPTER_PORT']


#loads lab_spec.json to retrieve lab_id,os,os_version,ram,diskspace etc.


try:
    lab_spec = json.loads(open("sample_lab_spec.json").read())
except IOError as e:
    print ("unable to load lab_spec.json. Exception: " + str(e))
    raise e
except  Exception as e:
    print("unable to parse lab_spec.json. Exception: " + str(e))
    raise e
lab_ID = lab_spec['lab']['description']['id']
os = lab_spec['lab']['runtime_requirements']['platform']['os']
os_version = lab_spec['lab']['runtime_requirements']['platform']['osVersion']
ram = lab_spec['lab']['runtime_requirements']['platform']['memory']['min_required']
diskspace = lab_spec['lab']['runtime_requirements']['platform']['storage']['min_required']
try:
   # Execute the SQL command
   cursor.execute('insert into adapter_server values("%s","%s","%s","%s","%s","%s", "%s")' % (lab_ID,os,os_version,ram,diskspace,adapter_name, adapter_port))
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# loads config.json, to retrieve server port number from controller_config 

try:
    config_spec = json.loads(open("./config/config.json").read())
except IOError as e:
    print ("unable to load config.json. Exception: " + str(e))
    raise e
except  Exception as e:
    print("unable to parse config.json. Exception: " + str(e))
    raise e


port = config_spec["CONTROLLER_CONFIG"]["SERVER_PORT"]
try:
   # Execute the SQL command
   cursor.execute('insert into controller_server values("%s")' % (port))
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
# disconnect from server
db.close()
