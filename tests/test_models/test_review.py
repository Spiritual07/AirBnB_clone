#!/usr/bin/python3
"""Unittests for Review Module.
Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import models
import os
from time import sleep
import unittest
from models.review import Review
from datetime import datetime

class TestReview_instantiation(unittest.TestCase):
    """
    Unittests for testing instantiation of the Review class.
    """

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        r = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(r))
        self.assertNotIn("place_id", r.__dict__)

    def test_user_id_is_public_class_attribute(self):
        r = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(r))
        self.assertNotIn("user_id", r.__dict__)

    def test_text_is_public_class_attribute(self):
        r = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(r))
        self.assertNotIn("text", r.__dict__)

    def test_two_reviews_unique_ids(self):
        r1 = Review()
        r2 = Review()
        self.assertNotEqual(r1.id, r2.id)

    def test_two_reviews_different_created_at(self):
        r1 = Review()
        sleep(0.05)
        r2 = Review()
        self.assertLess(r1.created_at, r2.created_at)

    def test_two_reviews_different_updated_at(self):
        r1 = Review()
        sleep(0.05)
        r2 = Review()
        self.assertLess(r1.updated_at, r2.updated_at)

    def test_str_representation(self):
        MyDate = datetime.today()
        MyDateRepr = repr(MyDate )
        r = Review()
        r.id = "607999"
        r.created_at = r.updated_at = MyDate 
        review_str = r.__str__()
        self.assertIn("[Review] (607999)", review_str)
        self.assertIn("'id': '607999'", review_str)
        self.assertIn("'created_at': " + MyDateRepr, review_str)
        self.assertIn("'updated_at': " + MyDateRepr, review_str)

    def test_args_unused(self):
        r = Review(None)
        self.assertNotIn(None, r.__dict__.values())

    def test_instantiation_with_kwargs(self):
        MyDate  = datetime.today()
        MyDate_iso = MyDate.isoformat()
        review = Review(id="607", created_at=MyDate_iso, updated_at=MyDate_iso)

        # Convert the created_at attribute to a datetime object
        review.created_at = datetime.fromisoformat(review.created_at)

        self.assertEqual(review.id, "607")
        self.assertEqual(review.created_at, MyDate)
        self.assertEqual(review.updated_at, MyDate)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """
    Unittests for testing save method of the Review class.
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
        r = Review()
        sleep(0.05)
        first_updated_at = r.updated_at
        r.save()
        self.assertLess(first_updated_at, r.updated_at)

    def test_two_saves(self):
        r = Review()
        sleep(0.05)
        first_updated_at = r.updated_at
        r.save()
        second_updated_at = r.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        r.save()
        self.assertLess(second_updated_at, r.updated_at)

    def test_save_with_arg(self):
        r = Review()
        with self.assertRaises(TypeError):
            r.save(None)

    def test_save_updates_file(self):
        r = Review()
        r.save()
        review_id = "Review." + r.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())


class TestReview_to_dict(unittest.TestCase):
    """
    Unittests for testing to_dict method of the Review class.
    """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        r = Review()
        self.assertIn("id", r.to_dict())
        self.assertIn("created_at", r.to_dict())
        self.assertIn("updated_at", r.to_dict())
        self.assertIn("__class__", r.to_dict())

    def test_to_dict_contains_added_attributes(self):
        r = Review()
        r.middle_name = "Osaretin"
        r.my_number = 607
        self.assertEqual("Osaretin", r.middle_name)
        self.assertIn("my_number", r.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        r = Review()
        review_dict = r.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        MyDate = datetime.today()
        r = Review()
        r.id = "607999"
        r.created_at = r.updated_at = MyDate 
        to_dict = {
            'id': '607999',
            '__class__': 'Review',
            'created_at': MyDate.isoformat(),
            'updated_at': MyDate.isoformat(),
        }
        self.assertDictEqual(r.to_dict(), to_dict)

    def test_contrast_to_dict_dunder_dict(self):
        r = Review()
        self.assertNotEqual(r.to_dict(), r.__dict__)

    def test_to_dict_with_arg(self):
        r = Review()
        with self.assertRaises(TypeError):
            r.to_dict(None)


if __name__ == "__main__":
    unittest.main()