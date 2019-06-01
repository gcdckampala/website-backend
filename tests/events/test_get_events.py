import json
from ..test_base import BaseTestCase


class TestGetEvents(BaseTestCase):

    def test_get_all_upcoming_events(self):
        """
        Get All UpComing Events
        """
        res = self.client.get('/api/v1/events/upcoming')
        self.assertEqual(res.status_code, 200)

    def test_get_all_past_events(self):
        """
        Get All Past Events
        """
        res = self.client.get('/api/v1/events/past')
        self.assertEqual(res.status_code, 200)

    def test_get_single_event(self):
        """
        Get Single Event
        """
        res = self.client.get('/api/v1/events/past')
        event_id = json.loads(res.data)[0]['id']
        resp = self.client.get(f"/api/v1/events/{event_id}")
        self.assertEqual(resp.status_code, 200)

    def test_get_event_comments(self):
        """
        Get All Event Comments
        """
        res = self.client.get('/api/v1/events/past')
        event_id = json.loads(res.data)[0]['id']
        resp = self.client.get(f"/api/v1/events/{event_id}/comments")
        self.assertEqual(resp.status_code, 200)
