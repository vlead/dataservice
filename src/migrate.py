from db import *
from sqlalchemy import create_engine
from mongoengine import fields
from mongoengine import *

e = create_engine('mysql://root:password@localhost/vlabs_database')

connect('veelabs')

for row in e.execute('select * from institutes'):
    instt=Institute(row[1], row[2], row[3]).save()

for row in e.execute('select * from disciplines'):
    disc=Discipline(row[1],row[2]).save()
    
for row in e.execute('select * from developers'):
    dev=Developer()
    dev.developer_name=row[1]
    dev.email_id=row=row[2]
    dev.institute_name=row[0]
    dev.save()

for row in e.execute('select * from experiments'):
    exp=Experiment()
    exp.exp_id=row[1]
    exp.exp_name = row[2].decode('iso-8859-1').encode('utf-8') 
    exp.content_url=row[3]
    exp.simulation_url=row[4]
    exp.save()

for row in e.execute('select * from technologies'):
    tech=Technology(row[1],row[2]).save()
    #print row[1],row[2] 
instidict={}
discidict={}
#list of institutes

for row in e.execute('select l.id,i.institute_name from institutes i, labs l where i.id=l.institute_id;'):
    lid=int(row[0])
    instidict[lid]=row[1]

for row in e.execute('select l.id,d.discipline_name from disciplines d, labs l where d.id=l.discipline_id;'):
    lid=int(row[0])
    discidict[lid]=row[1]

devdict={}
for row in e.execute('select l.id,d.developer_name from developers d, labs l, developers_engaged de where d.email_id=de.developer_id and de.lab_id=l.id;'):
    lid=int(row[0])
    if lid not in devdict:
        devdict[lid]=[row[1]]
    else :
        if row[1] not in devdict[lid]:
            devdict[lid].append(row[1])

techdict={}
for row in e.execute('select l.id,t.technology_name from technologies t, labs l, technologies_used tu where t.id=tu.tech_id and l.id=tu.lab_id;'):
    lid=int(row[0])
    if lid not in techdict:
        techdict[lid]=[row[1]]
    else :
        if row[1] not in techdict[lid]:
            techdict[lid].append(row[1])



for row in e.execute('select * from labs'):
    lab=Lab()
    lab.lab_id=row[1]
    lab.name=row[2]
    lab.repo_url=row[4]
    lab.sources_availables=row[5]
    lab.hosted_url=row[6]
    if "Yes" in row[7]:   #labs.lab_deployed in mysql
        lab.is_deployed=True
    elif row[7] == "No":
        lab.is_deployed=False
    lab.num_of_exps=row[8]
    if "Yes" in row[9]:   #labs.content in mysql
        lab.is_content=True
    elif row[9] == "No":
        lab.is_content=False
    if "Yes" in row[10]:   #labs.simulation in mysql
        lab.is_simulation=True
    elif row[10] == "No":
        lab.is_simulation=False
    
    lab.web_2_compliance=row[11]
    lab.type_of_lab=row[12]
    lab.auto_hostable=row[13]
    lab.remarks=row[14]
    lab.integration_level=row[15]
    lab.status=row[16]
    lid=int(row[0])
    #institute name
    for insti in Institute.objects(name=instidict[lid]):
      lab.institute=insti
    #discipline name 
    for disci in Discipline.objects(name=discidict[lid]):
      lab.discipline_name=disci
    
    #developers
    if lid in devdict:
        for i in devdict[lid]: 
            for devv in Developer.objects(developer_name=i):
                lab.developers.append(devv)
    #technologies
    if lid in techdict:
        for i in techdict[lid]: 
            for tekk in Technology.objects(name=i):
                print tekk.name
                lab.technologies_used.append(tekk)
    lab.save()
    #print lid, lab.developers



    
    


    

