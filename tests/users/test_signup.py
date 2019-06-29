

class TestSignUp:

    def test_user_creation(self, init_db, client, default_role ):
        """
        Testing for User creation
        """
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'username': 'Ayotwasapening',
                'email': 'test32@email.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code == 201

    def test_user_email_missing(self, init_db, client, default_role ):
        """
        Testing for Email Missing
        """
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'username': 'Ayotwasapening',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code == 400

    def test_user_username_missing(self, init_db, client, default_role ):
        """
        Testing for username Missing
        """
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'email': 'test32@email.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code == 400

    def test_user_password_missing(self, init_db, client, default_role ):
        """
        Testing for password Missing
        """
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'username': 'Ayotwasapening',
                'email': 'test32@email.com',
            }
        )
        assert res.status_code == 400

    def test_user_email_exists(self, init_db, client, new_test_user, default_role ):
        """
        Testing for User Email Exists
        """
        user = new_test_user.save()
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'username': 'Ayowasape',
                'email': 'test@email.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code == 400

    def test_user_username_exists(self, init_db, client, new_test_user, default_role ):
        """
        Testing for User Username Exists
        """
        user = new_test_user.save()
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'username': 'Ayowasap',
                'email': 'test2@email.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code == 400

    def test_invalid_password(self, init_db, client, default_role ):
        """
        Testing for Invalid Password Pattern
        """
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'username': 'Ayowasap',
                'email': 'test@email.com',
                'password': 'Cedri5'
            }
        )
        assert res.status_code == 400

    def test_invalid_email(self, init_db, client, default_role ):
        """
        Testing for Invalid Email Pattern
        """
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'username': 'Ayowasap',
                'email': 'testemail.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code == 400

    def test_short_username(self, init_db, client, default_role ):
        """
        Testing for Short username
        """
        role = default_role.save()
        res = client.post(
            'api/v1/auth/signup', 
            json={
                'username': 'Ayo',
                'email': 'test@email.com',
                'password': 'Cedric@25!'
            }
        )
        assert res.status_code == 400
