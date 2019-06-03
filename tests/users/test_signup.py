from ..test_base import BaseTestCase


class TestLogin(BaseTestCase):

    def test_user_creation(self):
        """
        Testing for User creation
        """
        res = self.register("test1234", "test1234@gmail.com", "test@1234")
        self.assertEqual(res.status_code, 201)

    def test_user_email_missing(self):
        """
        Testing for Email Missing
        """
        res = self.register("test12", None, "test@1234")
        self.assertEqual(res.status_code, 400)

    def test_user_username_missing(self):
        """
        Testing for username Missing
        """
        res = self.register(None, "test14@gmail.com", "test@1234")
        self.assertEqual(res.status_code, 400)

    def test_user_password_missing(self):
        """
        Testing for password Missing
        """
        res = self.register("test12", "test14@gmail.com", None)
        self.assertEqual(res.status_code, 400)

    def test_user_email_exists(self):
        """
        Testing for User Email Exists
        """
        self.register("testEmail", "test14@gmail.com", "test@1234")
        res = self.register("otheruser", "test14@gmail.com",  "test@1234")
        self.assertEqual(res.status_code, 400)

    def test_user_username_exists(self):
        """
        Testing for User Username Exists
        """
        self.register("testEmail", "test14@gmail.com", "test@1234")
        res = self.register("testEmail", "otheremail@gmail.com",  "test@1234")
        self.assertEqual(res.status_code, 400)

    def test_invalid_password(self):
        """
        Testing for Invalid Password Pattern
        """
        res = self.register("testEmail", "test14@gmail.com", "test")
        self.assertEqual(res.status_code, 400)

    def test_invalid_email(self):
        """
        Testing for Invalid Email Pattern
        """
        res = self.register("testEmail", "invalidemail",  "test@1234")
        self.assertEqual(res.status_code, 400)

    def test_short_username(self):
        """
        Testing for Short username
        """
        res = self.register("te", "test14@gmail.com",  "test@1234")
        print(res.data)
        self.assertEqual(res.status_code, 400)
