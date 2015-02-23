# -*- coding: utf-8 -*-

from sqlalchemy import create_engine

from src.app import create_app
from src.db import Technology, TechnologyUsed, Institute, Discipline,\
    Developer, Lab, DeveloperEngaged, Experiment

from src import config

old_db_uri = 'mysql+oursql://root:root@localhost/new_database'
old_db = create_engine(old_db_uri)
conn = old_db.connect()


app = create_app(config)


def populate_tech():
    print "Populating technologies table.."

    result = conn.execute('select * from technologies')
    for row in result:
        # id = row[0]
        name = row[1].strip()
        if row[2] == "Yes":
            foss = True
        elif row[2] == "No":
            foss = False
        else:
            foss = None

        new_tech = Technology(name=name, foss=foss)
        print new_tech.name, new_tech.foss
        new_tech.save()
    print "Done saving technologies.."


def populate_instt():
    print "Populating institutes table.."

    result = conn.execute('select * from institutes')
    for row in result:
        print 'id', 'name', 'coordinator', 'integration_coordinator'
        print row[0], row[1], row[2], row[3]
        if not row[3]:
            iic = None
        else:
            iic = row[3].strip()
        instt = Institute(name=row[1].strip(),
                          coordinator=row[2].strip(),
                          integration_coordinator=iic)
        print instt
        instt.save()
    print "Done saving institutes.."


def populate_disc():
    print "Populating disciplines table.."

    result = conn.execute('select * from disciplines')
    for row in result:
        print 'id', 'name', 'dnc'
        print row[0], row[1], row[2]
        name = row[1].strip()
        dnc = row[2].strip()

        if dnc == "Unknown":
            dnc = None
        disc = Discipline(name=name,
                          dnc=dnc)
        print disc
        disc.save()

    print "Done saving disciplines.."


def populate_devs():
    print "Populating developers table.."

    result = conn.execute('select * from developers')
    for row in result:
        if row[0] == "not known":
            continue

        print 'instt', 'name', 'email'
        print row[0], row[1], row[2]
        instt_name = row[0]
        if row[0] == "IIT Kharagpur":
            instt_name = "IIT-Kharagpur"

        instt = Institute.query.filter_by(name=instt_name).first()
        print instt
        print instt.id, instt.name
        dev = Developer(email_id=row[2].strip(),
                        name=row[1].strip(),
                        institute_id=instt.id)
        print dev
        dev.save()

    print "Done saving developers.."


def populate_labs():
    print "Populating labs table.."

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
            lab_id = None

        name = name.strip()

        # sanitize, normalize
        # TODO: review!
        if repo_url == "Unknown" or repo_url == "Unkown":
            repo_url = None

        # sanitize, normalize
        # TODO: review!
        if src_avail == "Yes":
            src_avail = True
        elif src_avail == "No":
            src_avail = False
        elif src_avail == "Partially Available":
            src_avail = False
            remarks += ' ;sources_available: Partially Available; '
        else:
            src_avail = None

        # sanitize, normalize
        # TODO: review!
        hosted_url = hosted_url.strip()
        if hosted_url.find('http') < 0:
            remarks += ' ;hosted_url: %s; ' % hosted_url
            hosted_url = None

        # sanitize, normalize
        # TODO: review!
        lab_deployed = lab_deployed.strip()
        if lab_deployed == "Yes":
            lab_deployed = True
        elif lab_deployed == "Yes, On Amrita":
            lab_deployed = True
            remarks += ' ;is_deployed: On Amrita; '
        elif lab_deployed == "No":
            lab_deployed = False
        else:
            lab_deployed = None

        # sanitize, normalize
        # TODO: review!
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
            remarks += ' ;is_simulation: %s; ' % simu
            simu = None
        else:
            remarks += ' ;is_simulation: %s; ' % simu
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
        simu_labs = ['Simulation Lab', 'Simuation Lab', 'Simulation']
        rt_labs = ['Remote Triggered', 'Remote Triggered  Lab (Pilot Phase)',
                   'Remote Triggered Lab', 'Remote Triggered Lab (Pilot phase)']
        if lab_type in simu_labs:
            lab_type = 'Simulation'
        elif lab_type in rt_labs:
            lab_type = 'Remote Triggered'
        elif lab_type == 'Simulation Lab + Remote Triggered':
            lab_type = 'Simulation Lab + Remote Triggered'
        elif lab_type == 'Unknown' or lab_type == "":
            lab_type = None
        elif lab_type == 'Pilot phase lab' or lab_type == 'pilot phase':
            lab_type = 'Pilot phase'

        # sanitize, normalize
        # TODO: review!
        auto_hostable = auto_hostable.strip()
        if auto_hostable == "Yes":
            auto_hostable = True
        elif auto_hostable == "No":
            auto_hostable = False
        else:
            auto_hostable = None

        if phase_2 == 1:
            phase_2 = True
        else:
            phase_2 = False

        # from the instt_id get the institute object
        instt = conn.execute('select * from institutes where id=%s' % inst_id)
        for row in instt:
            #print row[0], row[1], row[2]
            pass
        # from the name of the instt, get the id in the new db
        cur_instt = Institute.query.filter_by(name=row[1]).first()

        # from the disc_id get the institute object
        disc = conn.execute('select * from disciplines where id=%s' % disc_id)
        for row in disc:
            #print row[0], row[1], row[2]
            pass
        # from the name of the disc, get the id in the new db
        cur_disc = Discipline.query.filter_by(name=row[1]).first()

        print '===='
        print 'id', id
        print 'lab_id', lab_id
        print 'name', name
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
        print 'inst_id', cur_instt.id
        print 'disc_id', cur_disc.id
        print 'phase_2', phase_2
        print '===='
        #print raw_input('....')

        lab = Lab(lab_id=lab_id,
                  name=name,
                  repo_url=repo_url,
                  is_src_avail=src_avail,
                  hosted_url=hosted_url,
                  is_deployed=lab_deployed,
                  number_of_experiments=num_exps,
                  is_content_avail=content,
                  is_simulation=simu,
                  is_web_2_compliant=web_2_comp,
                  type_of_lab=lab_type,
                  is_auto_hostable=auto_hostable,
                  remarks=remarks,
                  integration_level=int_level,
                  status=status,
                  institute_id=cur_instt.id,
                  discipline_id=cur_disc.id,
                  is_phase_2_lab=phase_2)
        print lab
        try:
            lab.save()
        except Exception, e:
            print e
            raw_input('encountered exception. halted. press key to resume..')

    print "Done saving labs.."


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

        simu_url = row[4].strip()
        if simu_url.find('No') >= 0:
            simu_url = None

        exp = Experiment(lab_id=cur_lab.id,
                         name=row[2].strip(),
                         content_url=row[3].strip(),
                         simulation_url=simu_url)
        print exp
        exp.save()

    print "Done saving experiments.."


populate_tech()
populate_instt()
populate_disc()
populate_devs()
populate_labs()
populate_tech_used()
populate_dev_engaged()
populate_exps()

conn.close()
