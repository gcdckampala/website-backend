from flask import Blueprint, jsonify, request, json
from .models import MeetupAPIWrapper

events_app = Blueprint('events_app', __name__)
wrapper = MeetupAPIWrapper()


@events_app.route('/api/v1/events/upcoming')
def upcomingEvents():
    return jsonify(wrapper.getUpcomingEvents()), 200


@events_app.route('/api/v1/events/past')
def pastEvents():
    return jsonify(wrapper.getPastEvents()), 200


@events_app.route('/api/v1/events/<eventId>')
def singleEvent(eventId):
    return jsonify(wrapper.getSingleEvent(eventId)), 200


@events_app.route('/api/v1/events/<eventId>/comments')
def eventComment(eventId):
    return jsonify(wrapper.getEventComments(eventId)), 200
