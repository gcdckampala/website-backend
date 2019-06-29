

class TestLogin:

    def test_user_login_email(self, init_db, client, new_test_user ):
        """
        Testing for User Login
        """

        user = new_test_user.save()
        res = client.post(
            'api/v1/auth/login', 
            json={
                'email': 'test@email.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code == 200

    def test_user_login_username(self, init_db, client, new_test_user):
        """
        Testing for User Login
        """
        user = new_test_user.save()
        res = client.post(
            'api/v1/auth/login', 
            json={
                'username': 'Ayowasap',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code ==  200


    def test_login_wrong_password(self, init_db, client, new_test_user):
        """
        Testing for User Login Wrong Password
        """
        user = new_test_user.save()
        res = client.post(
            'api/v1/auth/login', 
            json={
                'email': 'test@email.com',
                'password': 'Cedric@25'
            }
        )
        assert res.status_code == 401

    def test_login_wrong_email(self, init_db, client, new_test_user):
        """
        Testing for User Login Wrong Email
        """
        user = new_test_user.save()
        res = client.post(
            'api/v1/auth/login', 
            json={
                'email': 'tes@email.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code ==  401

    def test_login_wrong_username(self, init_db, client, new_test_user):
        """
        Testing for User Login Wrong Username
        """
        user = new_test_user.save()
        res = client.post(
            'api/v1/auth/login', 
            json={
                'username': 'Ayy',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code ==  401

    def test_login_without_email(self, init_db, client, new_test_user):
        """
        Testing for User Login Wrong Username
        """
        user = new_test_user.save()
        res = client.post(
            'api/v1/auth/login', 
            json={
                'email': '',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code ==  400

    def test_login_with_username_and_email(self, init_db, client, new_test_user):
        """
        Testing for User Login Wrong Username
        """
        user = new_test_user.save()
        res = client.post(
            'api/v1/auth/login', 
            json={
                'username': 'Ayowasap',
                'email': 'tes@email.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code ==  400