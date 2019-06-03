from api.users.models import User
from application import create_app, db
import os
import sys
import unittest

sys.path.append(os.getcwd())


class BaseTestCase(unittest.TestCase):
    """This class represents the API test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            db.session.commit()

    def register(self, username, email, password):
        return self.client.post(
            'api/v1/auth/signup',
            json=dict(email=email, password=password, username=username),
        )

    def login_email(self, email, password):
        return self.client.post(
            'api/v1/auth/login',
            json=dict(email=email, password=password),
        )

    def login_username(self, username, password):
        return self.client.post(
            'api/v1/auth/login',
            json=dict(username=username, password=password),
        )

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
