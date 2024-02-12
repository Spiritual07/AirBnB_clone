#!/usr/bin/python3
"""Unittests for State Module.
Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import models
import os
from time import sleep
import unittest
from models.state import State
from datetime import datetime


class TestState_instantiation(unittest.TestCase):
    """
    Unittests for testing instantiation of the State class.
    """

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        s = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(s))
        self.assertNotIn("name", s.__dict__)

    def test_two_states_unique_ids(self):
        s1 = State()
        s2 = State()
        self.assertNotEqual(s1.id, s2.id)

    def test_two_states_different_created_at(self):
        s1 = State()
        sleep(0.05)
        s2 = State()
        self.assertLess(s1.created_at, s2.created_at)

    def test_two_states_different_updated_at(self):
        s1 = State()
        sleep(0.05)
        s2 = State()
        self.assertLess(s1.updated_at, s2.updated_at)

    def test_str_representation(self):
        MyDate = datetime.today()
        MyDateRepr = repr(MyDate)
        s = State()
        s.id = "607999"
        s.created_at = s.updated_at = MyDate
        s_str = s.__str__()
        self.assertIn("[State] (607999)", s_str)
        self.assertIn("'id': '607999'", s_str)
        self.assertIn("'created_at': " + MyDateRepr, s_str)
        self.assertIn("'updated_at': " + MyDateRepr, s_str)

    def test_args_unused(self):
        s = State(None)
        self.assertNotIn(None, s.__dict__.values())

    def test_instantiation_with_kwargs(self):
        MyDate = datetime.today()
        MyDate_iso = MyDate.isoformat()
        s = State(id="607", created_at=MyDate_iso, updated_at=MyDate_iso)

        # Convert the created_at attribute to a datetime object
        s.created_at = datetime.fromisoformat(s.created_at)

        self.assertEqual(s.id, "607")
        self.assertEqual(s.created_at, MyDate)
        self.assertEqual(s.updated_at, MyDate)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """
    Unittests for testing save method of the State class.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp.json")
        except FileNotFoundError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp.json", "file.json")
        except FileNotFoundError:
            pass

    def test_one_save(self):
        s = State()
        sleep(0.05)
        first_updated_at = s.updated_at
        s.save()
        self.assertLess(first_updated_at, s.updated_at)

    def test_two_saves(self):
        s = State()
        sleep(0.05)
        first_updated_at = s.updated_at
        s.save()
        second_updated_at = s.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        s.save()
        self.assertLess(second_updated_at, s.updated_at)

    def test_save_with_arg(self):
        s = State()
        with self.assertRaises(TypeError):
            s.save(None)

    def test_save_updates_file(self):
        s = State()
        s.save()
        s_id = "State." + s.id
        with open("file.json", "r") as f:
            self.assertIn(s_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """
    Unittests for testing to_dict method of the State class.
    """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        s = State()
        self.assertIn("id", s.to_dict())
        self.assertIn("created_at", s.to_dict())
        self.assertIn("updated_at", s.to_dict())
        self.assertIn("__class__", s.to_dict())

    def test_to_dict_contains_added_attributes(self):
        s = State()
        s.middle_name = "Osaretin"
        s.my_number = 607
        self.assertEqual("Osaretin", s.middle_name)
        self.assertIn("my_number", s.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        s = State()
        state_dict = s.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        MyDate = datetime.today()
        s = State()
        s.id = "607999"
        s.created_at = s.updated_at = MyDate
        tdict = {
            'id': '607999',
            '__class__': 'State',
            'created_at': MyDate.isoformat(),
            'updated_at': MyDate.isoformat(),
        }
        self.assertDictEqual(s.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        s = State()
        self.assertNotEqual(s.to_dict(), s.__dict__)

    def test_to_dict_with_arg(self):
        s = State()
        with self.assertRaises(TypeError):
            s.to_dict(None)


if __name__ == "__main__":
    unittest.main()
