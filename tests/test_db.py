# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
# import json
from src.db import *
from src.app import create_app

config = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+oursql://root:root@localhost:8080/vlabs_database'
}


class TestCustomTypes(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    # Test the Name type
    def test_name_type(self):
        print "test_name_type"
        new_name = Name("John")
        # correct name
        self.assertEqual(new_name.value, "John")
        # incorrect name
        self.assertRaises(TypeError, Name, "123dasd")

    # Test the Email type
    def test_correct_email_type(self):
        print "test_correct_email_type"
        new_email = Email("smith@gmail.com")
        # correct name
        self.assertEqual(new_email.value, "smith@gmail.com")
        # incorrect name
        self.assertRaises(TypeError, Email, "@@@@smithgmail.com")


class TestLab(TestCase):

    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def create_lab_prereqs(self):
    #    instt = Institute(name="MIT", mnemonic="mit")
    #    disc = Discipline(name="CS", mnemonic="cs")
    #    exp = Experiment(name="exp1")
    #    ilevel = IntegrationLevel(level=6)
    #    dev = Developer(name="Joe", institute=instt)

    def test_lab_get_lab_by_id(self):
        print "test_lab_get_lab_by_id"
        lab = Lab(name="DS", mnemonic="ds")
        lab.save()
        some_lab = Lab.get_lab_by_id(1)
        self.assertEqual(some_lab, lab)

    def test_lab_get_lab_by_mnemonic(self):
        print "test_lab_get_lab_by_mnemonic"
        lab = Lab(name="DS", mnemonic="ds")
        lab.save()
        some_lab = Lab.get_lab_by_mnemonic("ds")
        self.assertEqual(some_lab, lab)

    def test_lab_get_id(self):
        print "test_lab_get_id"
        lab = Lab(name="DS", mnemonic="ds")
        lab.save()
        self.assertEqual(lab.get_id(), 1)

    def test_lab_get_mnemonic(self):
        print "test_lab_get_mnemonic"
        lab = Lab(name="DS", mnemonic="ds")
        self.assertEqual(lab.get_mnemonic(), "ds")

    def test_lab_get_name(self):
        print "test_lab_get_name"
        lab = Lab(name="DS", mnemonic="ds")
        self.assertEqual(lab.get_name(), "DS")

    def test_lab_get_institute(self):
        print "test_lab_get_institute"
        instt = Institute(name="MIT", mnemonic="mit")
        lab = Lab(name="DS", mnemonic="ds", institute=instt)
        self.assertEqual(lab.get_institute().name, "MIT")

    def test_lab_get_integration_level(self):
        print "test_lab_get_integration_level"
        ilevel = IntegrationLevel(level=1)
        lab = Lab(name="DS", mnemonic="ds", integration_level=ilevel)
        self.assertEqual(lab.get_integration_level(), 1)

    def test_lab_get_hosted_url(self):
        print "test_lab_get_hosted_url"
        lab = Lab(name="DS", mnemonic="ds", hosted_url="http://gnu.org")
        self.assertEqual(lab.get_hosted_url(), "http://gnu.org")

    def test_lab_get_developers(self):
        print "test_lab_get_developers"
        dev1 = Developer(name="Joe")
        dev2 = Developer(name="Smith")
        devs = [dev1, dev2]
        lab = Lab(name="DS", mnemonic="ds", developers=devs)
        self.assertItemsEqual(lab.get_developers(), devs)

    def test_lab_get_technologies(self):
        print "test_lab_get_technologies"
        tech1 = Technology(name="php5")
        tech2 = Technology(name="apache2")
        techs = [tech1, tech2]
        lab = Lab(name="DS", mnemonic="ds", technologies=techs)
        self.assertItemsEqual(lab.get_technologies(), techs)


class TestDeveloper(TestCase):

    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Tests for developer entity
    def test_set_developer_name(self):
        print "test_set_developer_name"
        instt = Institute(name="MIT", mnemonic="mit")
        dev = Developer(name="Joe", institute=instt, email_id="joe@example.com")
        new_name = Name("John")
        # print "dev", new_name
        # print new_name, type(new_name)
        dev.set_name(new_name)
        self.assertEqual(dev.name, "John")
        self.assertRaises(TypeError, dev.set_name, "John")

    def test_set_developer_email(self):
        print "test_set_developer_email"
        instt = Institute(name="MIT", mnemonic="mit")
        dev = Developer(name="Joe", institute=instt, email_id="joe@example.com")
        # print dev
        new_email = Email("bob@gmail.com")
        # print new_email, type(new_email)
        dev.set_email(new_email)
        self.assertEqual(dev.email_id, "bob@gmail.com")
        self.assertRaises(TypeError, dev.set_email, "some@gmail.com")

    def test_get_developer_by_id(self):
        print "test_get_developer_by_id"
        instt = Institute(name="MIT", mnemonic="mit")
        dev = Developer(name="Joe", institute=instt, email_id="joe@example.com")
        dev.save()
        self.assertEqual(dev.get_developer(1).name, "Joe")

    def test_get_developer_email(self):
        print "test_get_developer_email"
        instt = Institute(name="MIT", mnemonic="mit")
        dev = Developer(name="Joe", institute=instt, email_id="joe@example.com")
        email_id = dev.get_email()
        self.assertEqual(email_id, "joe@example.com")

    def test_get_developer_name(self):
        print "test_get_developer_name"
        instt = Institute(name="MIT", mnemonic="mit")
        dev = Developer(name="Joe", institute=instt, email_id="joe@example.com")
        name = dev.get_name()
        self.assertEqual(name, "Joe")

   
class TestInstitute(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Tests for Institute entity.
    def test_set_institute_pic(self):
        print "test_set_institute_pic"
        instt = Institute(name="IndianInstitute", mnemonic="ii",
                          pic="Avinash", iic="Amit")
        new_pic = Name("John Doe")
        # print new_pic
        instt.set_pic(new_pic)
        self.assertEqual(instt.pic, "John Doe")

    def test_set_institute_iic(self):
        print "test_set_institute_iic"
        instt = Institute(name="IndianInstitute", mnemonic="ii",
                          pic="John", iic="Amit")
        new_iic = Name("Jane Doe")
        # print new_iic
        instt.set_iic(new_iic)
        self.assertEqual(instt.iic, "Jane Doe")

    def test_set_institute_name(self):
        print "test_set_institute_name"
        instt = Institute(name="IndianInstitute", mnemonic="ii",
                          pic="John", iic="Amit")
        new_name = InstituteName("IIT-Hyd Telangana")
        instt.set_name(new_name)
        self.assertEqual(instt.name, "IIT-Hyd Telangana")

    def test_get_institute_name(self):
        print "test_get_institute_name"
        instt = Institute(name="IndianInstitute", mnemonic="ii",
                          pic="John", iic="Jane")
        inst_name = instt.get_name()
        self.assertEqual(inst_name, "IndianInstitute")

    def test_get_institute_pic(self):
        print "test_get_institute_pic"
        instt = Institute(name="IndianInstitute", mnemonic="ii",
                          pic="John", iic="Jane")
        inst_pic = instt.get_pic()
        self.assertEqual(inst_pic, "John")

    def test_get_institute_iic(self):
        print "test_get_institute_iic"
        instt = Institute(name="IndianInstitute", mnemonic="ii",
                          pic="John", iic="Jane")
        inst_iic = instt.get_iic()
        self.assertEqual(inst_iic, "Jane")

    def test_get_id_of_institute(self):
        print "test_get_id_of_institute"
        instt = Institute(id="1", name="SomeInstitute", mnemonic="si")
        institute_id = instt.get_id()
        self.assertEqual(institute_id, "1")

    def test_get_institute_by_id(self):
        print "test_get_institute_by_id"
        instt = Institute(name="IndianInstitute", mnemonic="ii",
                          pic="John", iic="Jane")
        instt.save()
        self.assertEqual(instt.get_institute_by_id(1).name, "IndianInstitute")

    def test_get_institute_labs(self):
        print "test_get_institute_labs"
        lab1 = Lab(name="Micro Controllers", mnemonic="micro")
        lab2 = Lab(name="Digital Logic Design", mnemonic="digital")
        labs = [lab1, lab2]
        instt = Institute(name="MIT", mnemonic="mit", labs=labs)
        self.assertItemsEqual(instt.get_labs(), labs)
        
class TestDiscipline(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test for set_dnc attribute of Discipline entity
    def test_set_discipline_dnc(self):
        print "test_set_discipline_dnc"
        disc = Discipline(name="CSE", mnemonic="cs")
        new_dnc = Name("James roy")
        disc.set_dnc(new_dnc)
        self.assertEqual(disc.dnc, "James roy")
        self.assertRaises(TypeError, disc.set_dnc, "123 James roy")

    # Test for get_id attribute of Discipline entity
    def test_get_discipline_id(self):
        print "test_get_discipline_id"
        disc = Discipline(name="CSE", mnemonic="cs")
        disc.save()
        self.assertEqual(disc.id, disc.get_id())

    # Test for get_dnc attribute of Discipline entity
    def test_get_discipline_dnc(self):
        print "test_get_discipline_dnc"
        disc = Discipline(name="CSE", mnemonic="cs", dnc="James")
        self.assertEqual(disc.get_dnc(), "James")

    def test_get_discipline_by_id(self):
        print "test_get_discipline_name"
        disc = Discipline(name="CSE", mnemonic="cs", dnc="James")
        disc.save()
        self.assertEqual(disc.get_discipline_by_id(1).name, disc.name)

    def test_get_discipline_labs(self):
        print "test_get_discipline_labs"
        lab1 = Lab(name="Micro Controllers", mnemonic="micro")
        lab2 = Lab(name="Digital Logic Design", mnemonic="digital")
        labs = [lab1, lab2]
        disc = Discipline(name="Electronics", mnemonic="ece", labs=labs)
        self.assertItemsEqual(disc.get_labs(), labs)

if __name__ == '__main__':
    unittest.main()
