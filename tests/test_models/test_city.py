"""Unittests for City Module.
Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""

import models
import os
from time import sleep
import unittest
from models.city import City
from datetime import datetime


class TestCity_instantiation(unittest.TestCase):
    """
    Unittests for instantiation of the City class.
    """

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        c = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(c))
        self.assertNotIn("state_id", c.__dict__)

    def test_name_is_public_class_attribute(self):
        c = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(c))
        self.assertNotIn("name", c.__dict__)

    def test_two_cities_unique_ids(self):
        c1 = City()
        c2 = City()
        self.assertNotEqual(c1.id, c2.id)

    def test_two_cities_different_created_at(self):
        c1 = City()
        sleep(0.05)
        c2 = City()
        self.assertLess(c1.created_at, c2.created_at)

    def test_two_cities_different_updated_at(self):
        c1 = City()
        sleep(0.05)
        c2 = City()
        self.assertLess(c1.updated_at, c2.updated_at)

    def test_str_representation(self):
        MyDate = datetime.today()
        MyDateRepr = repr(MyDate)
        c = City()
        c.id = "607999"
        c.created_at = c.updated_at = MyDate
        city_str = c.__str__()
        self.assertIn("[City] (607999)", city_str)
        self.assertIn("'id': '607999'", city_str)
        self.assertIn("'created_at': " + MyDateRepr, city_str)
        self.assertIn("'updated_at': " + MyDateRepr, city_str)

    def test_args_unused(self):
        c = City(None)
        self.assertNotIn(None, c.__dict__.values())

    def test_instantiation_with_kwargs(self):
        MyDate = datetime.today()
        MyDate_iso = MyDate.isoformat()
        city = City(id="607", created_at=MyDate_iso, updated_at=MyDate_iso)

        # Convert the created_at attribute to a datetime object
        city.created_at = datetime.fromisoformat(city.created_at)

        self.assertEqual(city.id, "607")
        self.assertEqual(city.created_at, MyDate)
        self.assertEqual(city.updated_at, MyDate)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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
        c = City()
        sleep(0.05)
        first_updated_at = c.updated_at
        c.save()
        self.assertLess(first_updated_at, c.updated_at)

    def test_two_saves(self):
        c = City()
        sleep(0.05)
        first_updated_at = c.updated_at
        c.save()
        second_updated_at = c.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        c.save()
        self.assertLess(second_updated_at, c.updated_at)

    def test_save_with_arg(self):
        c = City()
        with self.assertRaises(TypeError):
            c.save(None)

    def test_save_updates_file(self):
        c = City()
        c.save()
        city_id = "City." + c.id
        with open("file.json", "r") as f:
            self.assertIn(city_id, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        c = City()
        self.assertIn("id", c.to_dict())
        self.assertIn("created_at", c.to_dict())
        self.assertIn("updated_at", c.to_dict())
        self.assertIn("__class__", c.to_dict())

    def test_to_dict_contains_added_attributes(self):
        c = City()
        c.middle_name = "Osaretin"
        c.my_number = 777
        self.assertEqual("Osaretin", c.middle_name)
        self.assertIn("my_number", c.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        c = City()
        city_dict = c.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        MyDate = datetime.today()
        c = City()
        c.id = "607999"
        c.created_at = c.updated_at = MyDate
        to_dict = {
            'id': '607999',
            '__class__': 'City',
            'created_at': MyDate.isoformat(),
            'updated_at': MyDate.isoformat(),
        }
        self.assertDictEqual(c.to_dict(), to_dict)

    def test_contrast_to_dict_dunder_dict(self):
        c = City()
        self.assertNotEqual(c.to_dict(), c.__dict__)

    def test_to_dict_with_arg(self):
        c = City()
        with self.assertRaises(TypeError):
            c.to_dict(None)


if __name__ == "__main__":
    unittest.main()
