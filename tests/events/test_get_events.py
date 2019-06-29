import json
# from ..test_base import BaseTestCase


class TestGetEvents:

    def test_get_all_upcoming_events(self, client):
        """
        Get All UpComing Events
        """
        res = client.get('/api/v1/events/upcoming')
        assert res.status_code == 200

    def test_get_all_past_events(self, client):
        """
        Get All Past Events
        """
        res = client.get('/api/v1/events/past')
        assert res.status_code == 200

    def test_get_single_event(self, client):
        """
        Get Single Event
        """
        res = client.get('/api/v1/events/past')
        event_id = json.loads(res.data)[0]['id']
        resp = client.get(f"/api/v1/events/{event_id}")
        assert res.status_code == 200

    def test_get_event_comments(self, client):
        """
        Get All Event Comments
        """
        res = client.get('/api/v1/events/past')
        event_id = json.loads(res.data)[0]['id']
        resp = client.get(f"/api/v1/events/{event_id}/comments")
        assert res.status_code == 200
