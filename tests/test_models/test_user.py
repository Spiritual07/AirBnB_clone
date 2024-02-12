#!/usr/bin/python3
"""Unittests for User Module.
Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import models
import os
from time import sleep
import unittest
from models.user import User
from datetime import datetime


class TestUser_instantiation(unittest.TestCase):
    """
    Unittests for testing instantiation of the User class.
    """

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        u1 = User()
        u2 = User()
        self.assertNotEqual(u1.id, u2.id)

    def test_two_users_different_created_at(self):
        u1 = User()
        sleep(0.05)
        u2 = User()
        self.assertLess(u1.created_at, u2.created_at)

    def test_two_users_different_updated_at(self):
        u1 = User()
        sleep(0.05)
        u2 = User()
        self.assertLess(u1.updated_at, u2.updated_at)

    def test_str_representation(self):
        MyDate = datetime.today()
        MyDateRepr = repr(MyDate)
        u1 = User()
        u1.id = "607999"
        u1.created_at = u1.updated_at = MyDate
        u1_str = u1.__str__()
        self.assertIn("[User] (607999)", u1_str)
        self.assertIn("'id': '607999'", u1_str)
        self.assertIn("'created_at': " + MyDateRepr, u1_str)
        self.assertIn("'updated_at': " + MyDateRepr, u1_str)

    def test_args_unused(self):
        u1 = User(None)
        self.assertNotIn(None, u1.__dict__.values())

    def test_instantiation_with_kwargs(self):
        MyDate = datetime.today()
        MyDate_iso = MyDate.isoformat()
        u1 = User(id="607", created_at=MyDate_iso, updated_at=MyDate_iso)

        # Convert the created_at attribute to a datetime object
        u1.created_at = datetime.fromisoformat(u1.created_at)

        self.assertEqual(u1.id, "607")
        self.assertEqual(u1.created_at, MyDate)
        self.assertEqual(u1.updated_at, MyDate)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save method of the  class."""

    @classmethod
    def setUpClass(self):
        try:
            os.rename("file.json", "tmp")
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp", "file.json")
        except FileNotFoundError:
            pass

    def test_one_save(self):
        u = User()
        sleep(0.05)
        updated_at1 = u.updated_at
        u.save()
        self.assertLess(updated_at1, u.updated_at)

    def test_two_saves(self):
        u = User()
        sleep(0.05)
        updated_at1 = u.updated_at
        u.save()
        updated_at2 = u.updated_at
        self.assertLess(updated_at1, updated_at2)
        sleep(0.05)
        u.save()
        self.assertLess(updated_at2, u.updated_at)

    def test_save_with_arg(self):
        u = User()
        with self.assertRaises(TypeError):
            u.save(None)

    def test_save_updates_file(self):
        u = User()
        u.save()
        u_id = "User." + u.id
        with open("file.json", "r") as f:
            self.assertIn(u_id, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        u = User()
        self.assertIn("id", u.to_dict())
        self.assertIn("created_at", u.to_dict())
        self.assertIn("updated_at", u.to_dict())
        self.assertIn("__class__", u.to_dict())

    def test_to_dict_contains_added_attributes(self):
        u = User()
        u.middle_name = "Osaretin"
        u.my_number = 98
        self.assertEqual("Osaretin", u.middle_name)
        self.assertIn("my_number", u.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        u = User()
        u_dict = u.to_dict()
        self.assertEqual(str, type(u_dict["id"]))
        self.assertEqual(str, type(u_dict["created_at"]))
        self.assertEqual(str, type(u_dict["updated_at"]))

    def test_to_dict_output(self):
        MyDate = datetime.today()
        u = User()
        u.id = "607999"
        u.created_at = u.updated_at = MyDate
        tdict = {
            'id': '607999',
            '__class__': 'User',
            'created_at': MyDate.isoformat(),
            'updated_at': MyDate.isoformat(),
        }
        self.assertDictEqual(u.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        u = User()
        self.assertNotEqual(u.to_dict(), u.__dict__)

    def test_to_dict_with_arg(self):
        u = User()
        with self.assertRaises(TypeError):
            u.to_dict(None)


if __name__ == "__main__":
    unittest.main()
