# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
# import json

from src.db import *
from src.app import create_app


class DBTest(TestCase):

    TESTING = True
    config = {
        'SQLALCHEMY_DATABASE_URI': ''
    }

    def create_app(self):
        app = create_app(self.config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_experiment(self):
        pass

    def test_set_developer_name(self):
        print "test_set_developer_name()"
        instt = Institute(name="MIT")
        dev = Developer(name="Joe", institute=instt, email_id="joe@example.com")
        new_name = Name("John")
        print "dev", new_name
        print new_name, type(new_name)
        dev.set_name(new_name)
        self.assertEqual(dev.name, "John")
        self.assertRaises(TypeError, dev.set_name, "John")

    def test_name_type(self):
        new_name = Name("John")
        self.assertEqual(new_name.value, "John")
        self.assertRaises(TypeError, Name, "123dasd")

    # Tests for Institute entity.
    def test_set_institute_pic(self):
        print "test_set_institute_pic()"
        instt = Institute(name="IndianInstitute", PIC="Avinash", IIC="Amit")
        new_pic = Name("John Doe")
        print new_pic
        instt.set_pic(new_pic)
        self.assertEqual(instt.PIC.value, "John Doe")

    def test_set_institute_iic(self):
        print "test_set_institute_iic()"
        instt = Institute(name="IndianInstitute", PIC="John", IIC="Amit")
        new_iic = Name("Jane Doe")
        print new_iic
        instt.set_iic(new_iic)
        self.assertEqual(instt.IIC.value, "Jane Doe")

    def test_set_institute_name(self):
        print "test_set_institute_name()"
        instt = Institute(name="IndianInstitute", PIC="John", IIC="Amit")
        new_name = InstituteName("IIT-Hyd Telangana")
        instt.set_name(new_name)
        self.assertEqual(instt.name.value, "IIT-Hyd Telangana")
        
    def test_get_institute_pic(self):
        print "test_get_institute_pic()"
        instt = Institute(name="IndianInstitute", PIC="John", IIC="Jane")
        inst_pic = instt.get_pic()
        self.assertEqual(inst_pic, "John")

    def test_get_institute_iic(self):
        print "test_get_institute_iic()"
        instt = Institute(name="IndianInstitute", PIC="John", IIC="Jane")
        inst_iic = instt.get_iic()
        self.assertEqual(inst_iic, "Jane")

    def test_get_id_of_institute(self):
        print "test_get_id_of_institute()"
        instt = Institute(id="1", name="SomeInstitute")
        institute_id = instt.get_id()
        self.assertEqual(institute_id, "1")

    def test_get_institute_by_id(self):
        print "test_get_institute_by_id()"
        instt = Institute(name="IndianInstitute", PIC="John", IIC="Jane")
        instt.save()
        self.assertEqual(instt.get_institute_by_id(1).name, "IndianInstitute")

  #  def test_get_institute_by_developer(self):
  #     print "test_get_institute_by_developer()"
  #     instt = Institute(name="IITHyd")
  #     instt.save()
  #     dev = Developer(name="John Doe", institute_id=instt.id)
  #     self.assertEqual(instt.get_institute_by_developer(dev).name, "IITHyd#")


  # Test for set_dnc attribute of Discipline entity
    def test_set_discipline_dnc(self):
        print "test_set_dnc()"
        disc = Discipline()
        new_dnc = Name("James roy")
        disc.set_discipline_dnc(new_dnc)
        self.assertEqual(disc.dnc, "James roy")
        self.assertRaises(TypeError, disc.set_discipline_dnc, "James roy")

    # Test for get_id attribute of Discipline entity
    def test_get_discipline_id(self):
        print "test_get_id()"
        disc = Discipline(id="2")
        self.assertEqual(disc.id, disc.get_discipline_id())

    # Test for get_dnc attribute of Discipline entity
    def test_get_discipline_dnc(self):
        print "test_get_dnc()"
        disc = Discipline(dnc="james")
        self.assertEqual(disc.dnc, disc.get_discipline_dnc())

    # Test for get_disc attribute of Discipline entity
    def test_get_discipline_name(self):
        print "test_get_disc()"
        disc = Discipline(name="CSE")
        disc.save()
        self.assertEqual(disc.get_discipline_name(1).name, disc.name)


if __name__ == '__main__':
    unittest.main()
