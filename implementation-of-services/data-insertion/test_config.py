#!/usr/bin/python
import json
#parameters retrieved from config.json file
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
print adapter_name
print adapter_port
#parameters retrieved from sample_lab_spec.json file
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
#swap = lab_spec['lab']['runtime_requirements']['platform']['memory']['swap']
print lab_ID
print os_version
print ram
print diskspace
#print swap
#parameters are retrieved from config.json which is inside config folder.
config_spec = json.loads(open("./config/config.json").read())
port = config_spec["CONTROLLER_CONFIG"]["SERVER_PORT"]
print port
