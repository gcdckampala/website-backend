from ..test_base import BaseTestCase


class TestLogin(BaseTestCase):

    def test_user_login_email(self):
        """
        Testing for User Login
        """
        self.register("newuser", "testnew@gmail.com", "test@1234")
        res = self.login_email("testnew@gmail.com", "test@1234")
        self.assertEqual(res.status_code, 200)

    def test_user_login_username(self):
        """
        Testing for User Login
        """
        self.register("newuser", "testnew@gmail.com", "test@1234")
        res = self.login_username("newuser", "test@1234")
        self.assertEqual(res.status_code, 200)

    def test_login_wrong_password(self):
        """
        Testing for User Login Wrong Password
        """
        self.register("newuser", "testnew@gmail.com", "test@1234")
        res = self.login_email("testnew@gmail.com", "test")
        self.assertEqual(res.status_code, 401)

    def test_login_wrong_email(self):
        """
        Testing for User Login Wrong Email
        """
        self.register("newuser", "testnew@gmail.com", "test@1234")
        res = self.login_email("testn@gmail.com", "test@1234")
        self.assertEqual(res.status_code, 401)

    def test_login_wrong_username(self):
        """
        Testing for User Login Wrong Username
        """
        self.register("newuser", "testnew@gmail.com", "test@1234")
        res = self.login_username("newuse", "test@1234")
        self.assertEqual(res.status_code, 401)

    def test_login_without_email(self):
        """
        Testing for User Login Wrong Username
        """
        self.register("newuser", "testnew@gmail.com", "test@1234")
        res = self.login_email(None, "test@1234")
        self.assertEqual(res.status_code, 400)

    def test_login_with_username_and_email(self):
        """
        Testing for User Login Wrong Username
        """
        self.register("newuser", "testnew@gmail.com", "test@1234")
        res = self.client.post(
            'api/v1/auth/login',
            json=dict(username="newuser",
                      email="testnew@gmail.com", password="test@1234"),
        )
        self.assertEqual(res.status_code, 400)
