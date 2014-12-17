dict = {"id": 1,"lab_id": "cse01","lab_name": "Data Structures","developer": "kkishore@iiit.ac.in","repo_url": "https://bitbucket.org/virtual-labs/cse01-ds_new","sources_available": "Yes","hosted_url": "http://virtual-labs.ac.in/labs/cse01/","lab_deployed": "Yes","number_of_experiments": 9,"content": "Yes","simulation": "Yes","web2.0_compliance": "No","type_of_lab": "","auto_hostable": "Yes","remarks": "Completed ","integration_level": 5,"status": "Hosted","institute_id": 4,"discipline_id": 6}
print 'replacing keys'
if dict.has_key('discipline_id') and dict.has_key('institute_id'):
    dict['discipline_name'] = dict.pop('discipline_id')
    dict['institute_name'] = dict.pop('institute_id')
print dict

print 'replacing values'

if dict['discipline_name'] == 6 and  dict['institute_name'] == 4:
    dict['discipline_name'] = "computer science"
    dict['institute_name'] = "IIITH"

print dict

