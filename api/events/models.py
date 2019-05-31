import requests
import os


class MeetupAPIWrapper():
    url = os.getenv('MEETUP_API_URL') + "/events"
    getEventsUrl = url + "?&sign=true&photo-host=secure"
    getSingleEventUrl = url + "/{}"

    def getUpcomingEvents(self):
        return requests.get(self.getEventsUrl).json()

    def getPastEvents(self):
        pastEvents = requests.get(
            self.getEventsUrl + "&desc=true&status=past"
        )
        return pastEvents.json()

    @classmethod
    def getSingleEvent(cls, eventId):
        return requests.get(
            cls.getSingleEventUrl.format(eventId) +
            "?&sign=true&photo-host=secure"
        ).json()

    @classmethod
    def getEventComments(cls, eventId):
        comments = requests.get(
            cls.getSingleEventUrl.format(eventId) + "/comments?&sign=true"
            "&photo-host=secure&desc=true"
        )
        return comments.json()
