from api.users.models import User
from application import create_app, db
import os
import sys
import unittest
import json


sys.path.append(os.getcwd())


class BaseTestCase(unittest.TestCase):
    """This class represents the API test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.test_user = {
            "username": "test",
            "email": "test@gmail.com",
            "password": "test@1234"
        }

        with self.app.app_context():
            db.create_all()
            db.session.commit()

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        """
        Testing for User creation
        """
        res = self.client.post('api/v1/auth/signup', json=self.test_user)
        self.assertEqual(res.status_code, 201)
