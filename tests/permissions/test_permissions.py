

class TestPermissions:

    def test_get_permissions_no_permissions_added(self, init_db, client):
        """
        Testing for User Login
        """
        res = client.get(
            'api/v1/permissions'
        )
        assert res.status_code == 404

    def test_get_permissions(self, init_db, client, new_permission ):
        """
        Testing for User Login
        """
        permission = new_permission.save()
        res = client.get(
            'api/v1/permissions'
        )
        assert res.status_code == 200

    def test_post_permission(self, init_db, client, auth_header):
        """
        Testing for User Login
        """
        res = client.post(
            'api/v1/permissions',
            headers=auth_header,
            json={
                "type": "create programs",
                "role_id": 1
            }
        )
        assert res.status_code == 201