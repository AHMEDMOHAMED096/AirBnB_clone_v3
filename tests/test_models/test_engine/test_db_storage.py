#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
from models.engine import db_storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Set up the test database """
        os.environ['HBNB_ENV'] = 'dev'
        os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
        os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """ Closes session after all tests """
        cls.storage.close()

    def setUp(self):
        """ Reloads database before each test """
        self.storage.reload()

    def test_all(self):
        """ Test all method """
        test_user = User()
        test_city = City()

        self.storage.new(test_user)
        self.storage.new(test_city)
        self.storage.save()

        all_objs = self.storage.all()
        self.assertIn(test_user.id, all_objs)
        self.assertIn(test_city.id, all_objs)

        all_users = self.storage.all(User)
        self.assertIn(test_user.id, all_users)
        self.assertNotIn(test_city.id, all_users)

    def test_new_save_delete(self):
        """ Test the new, save, and delete methods """
        new_amenity = Amenity(name="Test Amenity")
        self.storage.new(new_amenity)
        self.storage.save()

        retrieved_amenity = self.storage.get(Amenity, new_amenity.id)
        self.assertEqual(retrieved_amenity, new_amenity)

        self.storage.delete(new_amenity)
        self.storage.save()
        deleted_amenity = self.storage.get(Amenity, new_amenity.id)
        self.assertIsNone(deleted_amenity)

    def test_reload(self):
        """ Test reload method """
        new_state = State(name="Test State")
        self.storage.new(new_state)
        self.storage.save()

        retrieved_state = self.storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)

        self.storage.reload()
        reloaded_state = self.storage.get(State, new_state.id)
        self.assertEqual(reloaded_state, new_state)

    def test_close(self):
        """ Test close method """
        self.storage.close()
        with self.assertRaises(Exception):
            self.storage.get(State, "any_id")

    def test_get(self):
        """ Test get method """
        new_review = Review(text="Test Review")
        self.storage.new(new_review)
        self.storage.save()

        retrieved_review = self.storage.get(Review, new_review.id)
        self.assertEqual(retrieved_review, new_review)

    def test_count(self):
        """ Test count method """
        test_user_1 = User()
        test_user_2 = User()
        self.storage.new(test_user_1)
        self.storage.new(test_user_2)
        self.storage.save()

        all_count = self.storage.count()
        self.assertEqual(all_count, 2)

        user_count = self.storage.count(User)
        self.assertEqual(user_count, 2)
        amenity_count = self.storage.count(Amenity)
        self.assertEqual(amenity_count, 0)


if __name__ == '__main__':
    unittest.main()
