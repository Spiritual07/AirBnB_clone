#!/usr/bin/python3
"""Unittest for Place Module.
Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import models
import os
from time import sleep
import unittest
from models.place import Place
from datetime import datetime

class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(p))
        self.assertNotIn("city_id", p.__dict__)

    def test_user_id_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(p))
        self.assertNotIn("user_id", p.__dict__)

    def test_name_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(p))
        self.assertNotIn("name", p.__dict__)

    def test_description_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(p))
        self.assertNotIn("desctiption", p.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(p))
        self.assertNotIn("number_rooms", p.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(p))
        self.assertNotIn("number_bathrooms", p.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(p))
        self.assertNotIn("max_guest", p.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(p))
        self.assertNotIn("price_by_night", p.__dict__)

    def test_latitude_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(p))
        self.assertNotIn("latitude", p.__dict__)

    def test_longitude_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(p))
        self.assertNotIn("longitude", p.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        p = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(p))
        self.assertNotIn("amenity_ids", p.__dict__)

    def test_two_places_unique_ids(self):
        p1 = Place()
        p2 = Place()
        self.assertNotEqual(p1.id, p2.id)

    def test_two_places_different_created_at(self):
        p1 = Place()
        sleep(0.05)
        p2 = Place()
        self.assertLess(p1.created_at, p2.created_at)

    def test_two_places_different_updated_at(self):
        p1 = Place()
        sleep(0.05)
        p2 = Place()
        self.assertLess(p1.updated_at, p2.updated_at)

    def test_str_representation(self):
        MyDate = datetime.today()
        MyDateRepr = repr(MyDate)
        p = Place()
        p.id = "607999"
        p.created_at = p.updated_at = MyDate
        p_str = p.__str__()
        self.assertIn("[Place] (607999)", p_str)
        self.assertIn("'id': '607999'", p_str)
        self.assertIn("'created_at': " + MyDateRepr, p_str)
        self.assertIn("'updated_at': " + MyDateRepr, p_str)

    def test_args_unused(self):
        p = Place(None)
        self.assertNotIn(None, p.__dict__.values())

    def test_instantiation_with_kwargs(self):
        MyDate = datetime.today()
        MyDate_iso = MyDate.isoformat()
        place = Place(id="607", created_at=MyDate_iso, updated_at=MyDate_iso)

        # Convert the created_at attribute to a datetime object
        place.created_at = datetime.fromisoformat(place.created_at)

        self.assertEqual(place.id, "607")
        self.assertEqual(place.created_at, MyDate)
        self.assertEqual(place.updated_at, MyDate)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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
        p = Place()
        sleep(0.05)
        updated_at1 = p.updated_at
        p.save()
        self.assertLess(updated_at1, p.updated_at)

    def test_two_saves(self):
        p = Place()
        sleep(0.05)
        updated_at1 = p.updated_at
        p.save()
        updated_at2 = p.updated_at
        self.assertLess(updated_at1, updated_at2)
        sleep(0.05)
        p.save()
        self.assertLess(updated_at2, p.updated_at)

    def test_save_with_arg(self):
        p = Place()
        with self.assertRaises(TypeError):
            p.save(None)

    def test_save_updates_file(self):
        p = Place()
        p.save()
        p_id = "Place." + p.id
        with open("file.json", "r") as f:
            self.assertIn(p_id, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        p = Place()
        self.assertIn("id", p.to_dict())
        self.assertIn("created_at", p.to_dict())
        self.assertIn("updated_at", p.to_dict())
        self.assertIn("__class__", p.to_dict())

    def test_to_dict_contains_added_attributes(self):
        p = Place()
        p.middle_name = "Osaretin"
        p.my_number = 607
        self.assertEqual("Osaretin", p.middle_name)
        self.assertIn("my_number", p.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        p = Place()
        place_dict = p.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        MyDate = datetime.today()
        p = Place()
        p.id = "607999"
        p.created_at = p.updated_at = MyDate
        tdict = {
            'id': '607999',
            '__class__': 'Place',
            'created_at': MyDate.isoformat(),
            'updated_at': MyDate.isoformat(),
        }
        self.assertDictEqual(p.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        p = Place()
        self.assertNotEqual(p.to_dict(), p.__dict__)

    def test_to_dict_with_arg(self):
        p = Place()
        with self.assertRaises(TypeError):
            p.to_dict(None)


if __name__ == "__main__":
    unittest.main()