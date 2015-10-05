# -*- coding: utf-8 -*-

from sqlalchemy import create_engine

from src.app import create_app
from src.db import *

from src import config

old_db_uri = 'mysql+oursql://root:polarbear@localhost/vlabs_database'
old_db = create_engine(old_db_uri)
conn = old_db.connect()


app = create_app(config)


def populate_tech():
    print "Populating technologies table.."

    result = conn.execute('select * from technologies')
    for row in result:
        # id = row[0]
        print "row: %s" % row
        name = str(row[1].strip())
        if row[2] == "Yes":
            foss = True
        elif row[2] == "No":
            foss = False
        else:
            foss = None

        if not foss:
            new_tech = Technology(name=name)
        else:
            new_tech = Technology(name=name, foss=foss)
        print new_tech.name, new_tech.foss
        new_tech.save()
    print "Done saving technologies.."


def populate_instt():
    print "Populating institutes table.."

    instts = [
        ('iiith', 'IIIT Hyderabad', 'Prof. Jayanthi Sivaswamy',
            'jsivaswamy@iiit.ac.in', 'Prof. Raghu Reddy',
            'raghu.reddy@iiit.ac.in'),
        ('iitb', 'IIT Bombay', 'Prof. Anil Kulkarni', 'anil@ee.iitb.ac.in',
            'Prof. Santosh Norohna', 'noronha@che.iitb.ac.in'),
        ('iitd', 'IIT Delhi', 'Prof. Ranjan Bose', 'rbose.iitd@gmail.com',
            'Prof. Suresh Bhalla', 'sbhalla@civil.iitd.ac.in'),
        ('iitr', 'IIT Roorkee', 'Prof. Vinod Kumar',
            'gargpfce@iitr.ernet.in', 'Prof Vinod Kumar', 'vinodfee@gmail.com'),
        ('iitg', 'IIT Guwahati', 'Prof. Ratnajit Bhattacharjee',
            'ratnajit@iitg.ernet.in', 'Dr. Santosh Biswas',
            'santosh_biswas@iitg.ernet.in'),
        ('iitk', 'IIT Kanpur', 'Prof.  Kantesh Balani', 'kbalani@iitk.ac.in',
            'Prof. Kantesh Balani', 'kbalani@iitk.ac.in'),
        ('iitkgp', 'IIT Kharagpur', 'Prof. C S Kumar',
            'kumar@mech.iitkgp.ernet.in', None, None),
        ('iitm', 'IIT Madras', 'Prof. P Sriram', 'sriram@ae.iitm.ac.in',
            None, None),
        ('nitk', 'NIT Surathkal', 'Prof. K V Gangadharan',
            'kvganga@nitk.ac.in', 'Prof. K V Gangadharan', 'kvganga@nitk.ac.in'),
        ('amrita', 'Amrita University', 'Prof. Krishnashree Achuthan',
            'krishna@amrita.edu', 'Prof. Shyam Diwakar', 'shyam.diwakar@gmail.com'),
        ('coep', 'College of Engineering, Pune', 'Prof. Sudhir Agashe',
            'sda.instru@coep.ac.in', 'S. U Ghumbre', 'shashi.comp@coep.ac.in'),
        ('dei', 'Dayalbagh Educational Institute', 'Prof. Soami P Satsangee',
            'deiusic@gmail.com', 'Rahul Swarup Sharma', 'rahulswarup@rediffmail.com')
    ]

    for row in instts:
        args = {}
        args['institute_id'] = row[0]
        args['name'] = row[1].strip()
        args['pic'] = Name(row[2].strip())
        args['pic_email'] = Email(row[3].strip())
        if row[4]:
            args['iic'] = Name(row[4].strip())
        if row[5]:
            args['iic_email'] = Email(row[5].strip())

        instt = Institute(**args)
        print instt
        #instt.save()

    print "Done saving institutes.."


def populate_disc():
    print "Populating disciplines table.."

    discs = [
        ('aero', 'Aerospace Engineering', None, None),
        ('biotech', 'Biotechnology and Biomedical Engineering',
         'Prof. Bipin Nair', 'bipin@amrita.edu'),
        ('chem-engg', 'Chemical Engineering', 'Prof. Santosh Noronha',
         'noronha@che.iitb.ac.in'),
        ('chem', 'Chemical Sciences', 'Prof. Soami P Satsangee',
         'deiusic@gmail.com'),
        ('civil', 'Civil Engineering', 'Prof. P K Garg',
         'gargpfce@iitr.ernet.in'),
        ('cse', 'Computer Science and Engineering', 'Prof. Suresh Purini',
         'suresh.purini@iiit.ac.in'),
        ('ee', 'Electrical Engineering', 'Prof. Ratnajit Bhattacharjee',
         'ratnajit@iitg.ernet.in'),
        ('ece', 'Electronics and Communication', 'Prof. Mahesh Abegaonkar',
         'mpjosh@care.iitd.ernet.in'),
        ('hmt', 'Humanities', None, None),
        ('mech', 'Mechanical Engineering', 'Prof. C S Kumar',
         'kumar@mech.iitkgp.ernet.in'),
        ('phy-sc', 'Physical Sciences', 'Prof. Anjan Kumar Gupta',
         'anjankg@iitk.ac.in'),
        ('tex-engg', 'Textile Engineering', None, None),
        ('dsgn-engg', 'Design Engineering', None, None),
        ('mat-sc', 'Material Sciences', None, None)
    ]

    for row in discs:
        args = {}
        args['discipline_id'] = row[0]
        args['name'] = row[1].strip()
        if row[2]:
            args['dnc'] = Name(row[2].strip())
        if row[3]:
            args['dnc_email'] = Email(row[3].strip())

        disc = Discipline(**args)
        print disc
        disc.save()

    print "Done saving disciplines.."

instt_map = {
        'IIIT-H': 'iiith',
        'IIT-Bombay': 'iitb',
        'IIT Kharagpur': 'iitkgp',
        'IIT-Kharagpur': 'iitkgp',
        'IIT-Madras': 'iitm',
        'IIT-Delhi': 'iitd',
        'COEP': 'coep',
        'Dayalbagh': 'dei',
        'IIT-Kanpur': 'iitk',
        'IIT-Guwahati': 'iitg',
        'IIT-Roorkee': 'iitr',
        'NIT-K': 'nitk',
        'Amrita University': 'amrita'
    }

def populate_devs():
    print "Populating developers table.."

    result = conn.execute('select * from developers')
    for row in result:
        if row[0] == "not known":
            continue

        print 'instt', 'name', 'email'
        print row[0], row[1], row[2]
        instt_name = row[0]
        instt_id = instt_map[instt_name]

        instt = Institute.get_by_institute_id(instt_id)
        print instt
        print instt.id, instt.name
        dev = Developer(email=Email(row[2].strip()),
                        name=Name(row[1].strip()),
                        institute=instt)
        print dev
        dev.save()

    print "Done saving developers.."


def populate_labs():
    print "Populating labs table.."

    no_lab_id_ctr = 1

    result = conn.execute('select * from labs')
    for row in result:
        id = row[0]
        lab_id = row[1]
        name = row[2]
        dev = row[3]
        repo_url = row[4]
        src_avail = row[5]
        hosted_url = row[6]
        lab_deployed = row[7]
        num_exps = row[8]
        content = row[9]
        simu = row[10]
        web_2_comp = row[11]
        lab_type = row[12]
        auto_hostable = row[13]
        remarks = row[14]
        int_level = row[15]
        status = row[16]
        inst_id = row[17]
        disc_id = row[18]
        phase_2 = row[19]

        print '===='
        print 'id', id
        print 'lab_id', lab_id
        print 'name', name
        print 'developer', dev
        print 'repo_url', repo_url
        print 'src_avail', src_avail
        print 'hosted_url', hosted_url
        print 'lab_deployed', lab_deployed
        print 'num_exps', num_exps
        print 'content', content
        print 'simu', simu
        print 'web_2_comp', web_2_comp
        print 'type', lab_type
        print 'auto_hostable', auto_hostable
        print 'remarks', remarks
        print 'int_level', int_level
        print 'status', status
        print 'inst_id', inst_id
        print 'disc_id', disc_id
        print 'phase_2', phase_2
        print '===='

        lab_id = lab_id.strip()
        if lab_id == "Unknown":
            #lab_id = None
            lab_id = 'no_lab_id' + str(no_lab_id_ctr)
            no_lab_id_ctr += 1

        name = str(name.strip())

        # sanitize, normalize
        # TODO: review!
        repo_url = repo_url.strip()
        if repo_url == "Unknown" or repo_url == "Unkown":
            repo_url = None

        # sanitize, normalize
        # TODO: review!
        # add to remarks
        if src_avail == "Yes":
            pass
        elif src_avail == "No":
            pass
        elif src_avail == "Partially Available":
            remarks += ' ;sources_available: Partially Available; '

        # sanitize, normalize
        # TODO: review!
        hosted_url = hosted_url.strip()
        if hosted_url.find('http') < 0:
            remarks += ' ;hosted_url: %s; ' % hosted_url
            hosted_url = None
        if hosted_url == "Link is redirecting to http://vlab.co.in/institute_detail.php?ins=003 , Unable to view the lab":
            hosted_url = "http://vlab.co.in/institute_detail.php?ins=003"
            remarks += " ;hosted_url: Link is redirecting to http://vlab.co.in/institute_detail.php?ins=003 , Unable to view the lab"

        # sanitize, normalize
        # TODO: review!
        # add to remarks
        lab_deployed = lab_deployed.strip()
        if lab_deployed == "Yes":
            pass
        elif lab_deployed == "Yes, On Amrita":
            pass
            remarks += ' ;is_deployed: On Amrita; '
        elif lab_deployed == "No":
            pass
        else:
            pass

        # sanitize, normalize
        # TODO: review!
        # add to remarks
        content = content.strip()
        if content == "No":
            content = False
        elif content == "Unknown":
            content = None
        elif content == "Yes":
            content = True
        else:
            remarks += ' ;is_content_avail: %s; ' % content
            content = True

        # sanitize, normalize
        # TODO: review!
        simu = simu.strip()
        if simu == "No":
            simu = False
        elif simu == "Unknown":
            simu = None
        elif simu == "Yes":
            simu = True
        elif simu.find('Unable') >= 0:
            remarks += ' ;is_simulation_avail: %s; ' % simu
            simu = None
        else:
            remarks += ' ;is_simulation_avail: %s; ' % simu
            simu = True

        # sanitize, normalize
        # TODO: review!
        web_2_comp = web_2_comp.strip()
        if web_2_comp == "Yes":
            web_2_comp = True
        elif web_2_comp == "No":
            web_2_comp = False
        else:
            web_2_comp = None

        # sanitize, normalize
        # TODO: review!
        lab_type = lab_type.strip()
        simu_labs = ['Simulation Lab', 'Simuation Lab', 'Simulation',
                     'simulation lab']
        rt_labs = ['Remote Triggered', 'Remote Triggered  Lab (Pilot Phase)',
                   'Remote Triggered Lab', 'Remote Triggered Lab (Pilot phase)']
        if lab_type in simu_labs:
            lab_type = TypeOfLab.get_by_type('Simulation')
            #lab_type = 'Simulation'
        elif lab_type in rt_labs:
            #lab_type = 'Remote Triggered'
            lab_type = TypeOfLab.get_by_type('Remote Triggered')
        elif lab_type == 'Simulation Lab + Remote Triggered':
            #lab_type = 'Simulation Lab + Remote Triggered'
            lab_type = TypeOfLab.get_by_type('Simulation and Remote Triggered')
        elif lab_type == 'Unknown' or lab_type == "":
            lab_type = None
        elif lab_type == 'Pilot phase lab' or lab_type == 'pilot phase':
            #lab_type = 'Pilot phase'
            lab_type = TypeOfLab.get_by_type('Pilot Phase')

        if phase_2 == 1:
            phase_2 = True
        else:
            phase_2 = False

        # from the instt_id get the institute object
        instt = conn.execute('select * from institutes where id=%s' % inst_id)
        for row in instt:
            #print row[0], row[1], row[2]
            pass
        # from the name of the instt, get the instt_id and then get the instt
        # obj in the new db
        cur_instt = Institute.get_by_institute_id(instt_map[row[1]])

        # from the disc_id get the institute object
        disc = conn.execute('select * from disciplines where id=%s' % disc_id)
        for row in disc:
            print "name: %s" % row[1]
            disc_name = row[1].strip()
            if disc_name == "Electronics and Communications":
                disc_name = "Electronics and Communication"

        if disc_name == "Unknown":
            cur_disc = None
        else:
            # from the name of the disc, get the id in the new db
            cur_disc = Discipline.query.filter_by(name=disc_name).first()

        print "cur disc"
        print cur_disc

        # get the integration level obj from the level
        int_level = IntegrationLevel.get_by_level(int_level)

        # get this lab's developers
        devels = []
        devs = conn.execute('select * from developers_engaged where lab_id=%s' %
                            id)
        for row in devs:
            #email id is row[2]
            dev = Developer.query.filter_by(email=row[2]).first()
            devels.append(dev)

        # get this lab's technologies
        techs = []
        result = conn.execute('select a.lab_id, a.tech_id, b.technology_name '
                              'from technologies_used a, technologies b where '
                              'a.tech_id=b.id and lab_id=' + str(id))
        for row in result:
            #tech name is row[2]
            tech = Technology.query.filter_by(name=row[2]).first()
            techs.append(tech)

        print '===='
        print 'id', id
        print 'lab_id', lab_id
        print 'name', name
        print 'repo_url', repo_url
        print 'hosted_url', hosted_url
        print 'web_2_comp', web_2_comp
        print 'type', lab_type
        print 'remarks', remarks
        print 'int_level', int_level
        print 'status', status
        print 'inst_id', cur_instt.id
        print 'disc_id', cur_disc.id if cur_disc else None,
        print 'phase_2', phase_2
        print 'developers', devels
        print 'technologies', techs
        print '===='
        #print raw_input('....')

        args = {}
        args['lab_id'] = lab_id
        args['name'] = name
        args['institute'] = cur_instt
        if cur_disc:
            args['discipline'] = cur_disc
        args['integration_level'] = int_level
        if repo_url:
            args['repo_url'] = URL(repo_url)
        if hosted_url:
            args['hosted_url'] = URL(hosted_url)
        if lab_type:
            args['type_of_lab'] = lab_type
        if remarks:
            args['remarks'] = str(remarks)
        if status:
            args['status'] = str(status)
        if web_2_comp:
            args['is_web_2_compliant_lab'] = web_2_comp
        if phase_2:
            args['is_phase_2_lab'] = phase_2
        if len(devels):
            args['developers'] = devels
        if len(techs):
            args['technologies'] = techs

        lab = Lab(**args)
        print lab
        try:
            lab.save()
        except Exception, e:
            print e
            raw_input('encountered exception. halted. press key to resume..')

    print "Done saving labs.."


def populate_exps():
    print "Populating experiments table.."

    result = conn.execute('select * from experiments')
    for row in result:
        print 'lab_id', 'id', 'name', 'content_url', 'simulation_url'
        print row[0], row[1], row[2], row[3], row[4]

        lab = conn.execute('select * from labs where id=%s' % row[0])
        for nrow in lab:
            #print nrow[0], nrow[1], nrow[2], nrow[3]
            pass
        #print nrow[2]
        cur_lab = Lab.query.filter_by(name=nrow[2].strip()).first()
        print cur_lab
        print cur_lab.name, cur_lab.lab_id

        exp_name = row[2].strip()
        iso885915_utf_map = {
                u"\u2019":  u"'",
                u"\u2018":  u"'",
                u"\u201c":  u'"',
                u"\u201d":  u'"'
        }
        utf_map = dict([(ord(k), ord(v)) for k,v in iso885915_utf_map.items()])
        exp_name = exp_name.translate(utf_map).encode('iso-8859-15')
        # for the particular exp with id 1553 in the old database, change the
        # name
        if row[1] == 1553 and "\xa0" in exp_name:
            exp_name = "Relationship between guide ?g and ?a"
        exp_name = str(exp_name)
        print exp_name

        content_url = row[3].strip()
        # formatting errors in URL
        if content_url == "cp.freehostia.com/login/":
            content_url = "http://cp.freehostia.com/login/"
        if content_url == "iitkgp.vlab.co.in/?sub=37&brch=110&sim=243&cnt=512":
            content_url = "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=243&cnt=512"
        if content_url == "iitkgp.vlab.co.in/?sub=79&brch=262&sim=1299&cnt=1":
            content_url = "http://iitkgp.vlab.co.in/?sub=79&brch=262&sim=1299&cnt=1"

        # WRONG content URLs in the old database!!!!!!!!!!!!!
        # I had to manually find out the correct ones, and hard code them here!!
        if content_url == "http://amrita.vlab.co.in/?sub=3&brch=187&sim=878&cnt=1"\
                and exp_name == "Isolation of Mitochondria":
            content_url = "http://vlab.amrita.edu/?sub=3&brch=187&sim=327&cnt=2"
        if content_url == "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=252&cnt=7"\
                and exp_name == "Thickness Measurement Using Ellipsometer":
            content_url = "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=253&cnt=7"
        if content_url == "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=253&cnt=7"\
                and exp_name == "MOSFET SPICE Parameter Extraction":
            content_url = "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=254&cnt=7"
        if content_url == "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=255&cnt=7"\
                and exp_name == "Determination of Vth of a MOSFET":
            content_url = "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=256&cnt=7"
        if content_url == "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=255&cnt=7"\
                and exp_name == "JFET Characterization":
            content_url = "http://iitkgp.vlab.co.in/?sub=37&brch=110&sim=257&cnt=7"
        if content_url == "http://vls1.iitkgp.ernet.in/vls_web/experiments/experiment.php?expId=234"\
                and exp_name == "Position Analysis of a 4 Bar RRRR Non Grashofian D":
            content_url = "http://vls1.iitkgp.ernet.in/vls_web/experiments/experiment.php?expId=235"

        if content_url.find('No content') >= 0 or\
                content_url.find('deploy.v') >= 0:
            content_url = None

        simu_url = row[4].strip()
        if simu_url == "http://iitkgp.vlab.co.in/?sub=39&brch=125&sim=637&cnt=4"\
                and exp_name == "DF-Part6: Interrupt driven data transfer from ADC":
            simu_url = "http://iitkgp.vlab.co.in/?sub=39&brch=125&sim=1228&cnt=4"
        if simu_url == "http://vls1.iitkgp.ernet.in/vls_web/experiments/experiment.php?expId=234#"\
                and exp_name == "Position Analysis of a 4 Bar RRRR Non Grashofian D":
            simu_url = "http://vls1.iitkgp.ernet.in/vls_web/experiments/experiment.php?expId=235#"
        if simu_url == "http://iitd.vlab.co.in/?sub=67&brch=185&sim=470&cnt=4"\
                and exp_name == "DC Motor Speed Control":
            simu_url = "http://iitd.vlab.co.in/?sub=67&brch=185&sim=473&cnt=4"
        if simu_url == "http://iitd.vlab.co.in/?sub=67&brch=185&sim=473&cnt=4"\
                and exp_name == "Induction Motor Starting and Braking":
            simu_url = "http://iitd.vlab.co.in/?sub=67&brch=185&sim=1014&cnt=4"
        if simu_url == "http://iitd.vlab.co.in/?sub=67&brch=185&sim=1014&cnt=4"\
                and exp_name == "V/F Control Of VSI Fed Three-Phase Induction Motor":
            simu_url = "http://iitd.vlab.co.in/?sub=67&brch=185&sim=1046&cnt=4"
        if simu_url == "http://iitd.vlab.co.in/?sub=65&brch=180&sim=294&cnt=1478"\
                and exp_name == "Experiment of Microwave Cavity":
            simu_url = "http://iitd.vlab.co.in/?sub=65&brch=180&sim=295&cnt=1481"

        if simu_url.find('No simulation') >= 0 or\
                simu_url.find('Link not found') >= 0 or\
                simu_url.find('deploy.v') >= 0:
            simu_url = None

        args = {}
        args['lab'] = cur_lab
        args['name'] = exp_name
        if content_url:
            args['content_url'] = URL(content_url)
        if simu_url:
            args['simulation_url'] = URL(simu_url)

        exp = Experiment(**args)
        print exp
        #exp.save()

    print "Done saving experiments.."


#populate_tech()
#populate_instt()
#populate_disc()
#populate_devs()
#populate_labs()
populate_exps()

conn.close()

"""
def populate_tech_used():
    print "Populating technologies_used table.."

    result = conn.execute('select * from technologies_used')
    for row in result:
        print 'id', 'lab_id', 'tech_id', 'server_side', 'client_side'
        print row[0], row[1], row[2], row[3], row[4]

        lab = conn.execute('select * from labs where id=%s' % row[1])
        for nrow in lab:
            #print nrow[0], nrow[1], nrow[2], nrow[3]
            pass
        #print nrow[2]
        cur_lab = Lab.query.filter_by(name=nrow[2].strip()).first()

        tech = conn.execute('select * from technologies where id=%s' % row[2])
        for nrow in tech:
            #print nrow[0], nrow[1], nrow[2]
            pass
        #print nrow[1]
        cur_tech = Technology.query.filter_by(name=nrow[1].strip()).first()

        print cur_lab.id, cur_lab.name
        print cur_tech.id, cur_tech.name

        tech_used = TechnologyUsed(lab_id=cur_lab.id,
                                   tech_id=cur_tech.id,
                                   server_side=row[3],
                                   client_side=row[4])

        print tech_used.lab_id, tech_used.tech_id, tech_used.server_side
        #raw_input('..')
        # not working fails on some cur_lab.id
        tech_used.save()

    print "Done saving technologies_used.."


def populate_dev_engaged():
    print "Populating developers_engaged table.."
    result = conn.execute('select * from developers_engaged')
    for row in result:
        print 'id', 'lab id', 'dev email'
        print row[0], row[1], row[2]

        lab = conn.execute('select * from labs where id=%s' % row[1])
        for nrow in lab:
            #print nrow[0], nrow[1], nrow[2], nrow[3]
            pass
        #print nrow[2]
        cur_lab = Lab.query.filter_by(name=nrow[2].strip()).first()

        cur_dev = Developer.query.filter_by(email_id=row[2].strip()).first()

        print cur_lab.id, cur_lab.name
        print cur_dev.id, cur_dev.email_id

        dev_engaged = DeveloperEngaged(lab_id=cur_lab.id,
                                       developer_id=cur_dev.id)
        print dev_engaged
        dev_engaged.save()

    print "Done saving developers_engaged.."
"""
