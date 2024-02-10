#!/usr/bin/python3
"""Unittest for Amenity Module.
Unittest classes:
    TestAmenity_save
    TestAmenity_to_dict
    TestAmenity_instantiation
"""
import models
import os
from time import sleep
import unittest
from models.amenity import Amenity
from datetime import datetime

class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except FileNotFoundError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp", "file.json")
        except FileNotFoundError:
            pass

    def test_one_save(self):
        a = Amenity()
        sleep(0.05)
        updated_at1 = a.updated_at
        a.save()
        self.assertLess(updated_at1, a.updated_at)

    def test_two_saves(self):
        a = Amenity()
        sleep(0.05)
        updated_at1 = a.updated_at
        a.save()
        updated_at2 = a.updated_at
        self.assertLess(updated_at1, updated_at2)
        sleep(0.05)
        a.save()
        self.assertLess(updated_at2, a.updated_at)

    def test_save_with_arg(self):
        a = Amenity()
        with self.assertRaises(TypeError):
            a.save(None)

    def test_save_updates_file(self):
        a = Amenity()
        a.save()
        a_id = "Amenity." + a.id
        with open("file.json", "r") as f:
            self.assertIn(a_id, f.read())

class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        a = Amenity()
        self.assertIn("id", a.to_dict())
        self.assertIn("created_at", a.to_dict())
        self.assertIn("updated_at", a.to_dict())
        self.assertIn("__class__", a.to_dict())

    def test_to_dict_contains_added_attributes(self):
        a = Amenity()
        a.middle_name = "Osaretin"
        a.my_number = 607
        self.assertEqual("Osaretin", a.middle_name)
        self.assertIn("my_number", a.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        a = Amenity()
        a_dict = a.to_dict()
        self.assertEqual(str, type(a_dict["id"]))
        self.assertEqual(str, type(a_dict["created_at"]))
        self.assertEqual(str, type(a_dict["updated_at"]))

    def test_to_dict_output(self):
        MyDate = datetime.today()
        a = Amenity()
        a.id = "607999"
        a.created_at = a.updated_at = MyDate
        tdict = {
            'id': '607999',
            '__class__': 'Amenity',
            'created_at': MyDate.isoformat(),
            'updated_at': MyDate.isoformat(),
        }
        self.assertDictEqual(a.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        a = Amenity()
        self.assertNotEqual(a.to_dict(), a.__dict__)

    def test_to_dict_with_arg(self):
        a = Amenity()
        with self.assertRaises(TypeError):
            a.to_dict(None)
    
class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        a = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", a.__dict__)

    def test_two_amenities_unique_ids(self):
        a1 = Amenity()
        a2 = Amenity()
        self.assertNotEqual(a1.id, a2.id)

    def test_two_amenities_different_created_at(self):
        a1 = Amenity()
        sleep(0.05)
        a2 = Amenity()
        self.assertLess(a1.created_at, a2.created_at)

    def test_two_amenities_different_updated_at(self):
        a1 = Amenity()
        sleep(0.05)
        a2 = Amenity()
        self.assertLess(a1.updated_at, a2.updated_at)

    def test_str_representation(self):
        MyDate = datetime.today()
        MyDateRepr = repr(MyDate)
        a = Amenity()
        a.id = "607999"
        a.created_at = a.updated_at = MyDate
        a_str = a.__str__()
        self.assertIn("[Amenity] (607999)", a_str)
        self.assertIn("'id': '607999'", a_str)
        self.assertIn("'created_at': " + MyDateRepr, a_str)
        self.assertIn("'updated_at': " + MyDateRepr, a_str)

    def test_args_unused(self):
        a = Amenity(None)
        self.assertNotIn(None, a.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        MyDate = datetime.today()
        MyDate_iso = MyDate.isoformat()
        a = Amenity(id="607", created_at=MyDate_iso, updated_at=MyDate_iso)

        # Convert the created_at attribute to a datetime object
        a.created_at = datetime.fromisoformat(a.created_at)

        self.assertEqual(a.id, "607")
        self.assertEqual(a.created_at, MyDate)
        self.assertEqual(a.updated_at, MyDate)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

if __name__ == "__main__":
    unittest.main()