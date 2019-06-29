from api.roles.models import Roles


class TestRoles:

    def test_get_roles_no_roles_added(self, init_db, client):
        """
        Testing for User Login
        """
        res = client.get(
            'api/v1/roles'
        )
        assert res.status_code == 404

    def test_get_roles(self, init_db, client, default_role ):
        """
        Testing for User Login
        """
        role = default_role.save()
        res = client.get(
            'api/v1/roles'
        )
        assert res.status_code == 200

    def test_post_role(self, init_db, client, auth_header):
        """
        Testing for User Login
        """
        res = client.post(
            'api/v1/roles',
            headers=auth_header,
            json={
                'title': 'Regular user1',
                'description': 'This guy can actually hahah'
            }
        )
        assert res.status_code == 201