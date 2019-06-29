from flask import Blueprint, jsonify, request
from .models import User, UserSchema
import random
import string
from google.auth.transport import requests
from google.oauth2 import id_token

user_app = Blueprint('user_app', __name__)


@user_app.route("/api/v1/users")
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(
        {'users': user_schema.dump(users).data}), 200


@user_app.route("/api/v1/users/<username>")
def get_user(username):
    user = User.get_user(username=username).first()
    if user:
        user_schema = UserSchema()
        return jsonify(
            {'user': user_schema.dump(user).data}), 200
    return jsonify({'error': 'Invalid username'}), 400


@user_app.route("/api/v1/auth/signup", methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    try:
        # check that user with similar email exists
        check_user_exists(email)

        user = User(username=username, email=email, password=password)
        user.save()
        return jsonify({'username': user.username}), 201
    except AssertionError as exception_message:
        return jsonify(error=f"{exception_message}."), 400

def check_user_exists(email):
    try:
        if User.get_user(email=email).first():
            raise AssertionError('Email is already in use')
    except AttributeError:
        pass


@user_app.route("/api/v1/auth/login", methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    both_fields_missing = not username and not email
    both_fields_present = username and email
    three_fields_present = both_fields_present and password

    if both_fields_present or three_fields_present:
        return jsonify(
            {"error":
             "Please use either username or email to login but not both!"}
        ), 400

    else:
        return handle_response(both_fields_missing, username,
                               email, password)


def handle_response(*args):
    both_fields_missing, username, email, password = args

    if not password:
        return jsonify(
            {"error":
             "Username/Email and Password are required to login"}
        ), 400

    if both_fields_missing:
        email_username_missing_response = {
            'error': 'Either email or username field is required for login.'}
        return (jsonify(email_username_missing_response), 400)
    else:
        return login_helper(username, email, password)


def login_helper(*args):
    username, email, password = args
    password_missing_response = {'error': 'Password is required for login.'}
    if username:
        user = User.get_user(username=username).first()
        return handle_wrong_username_email(
            user, password, password_missing_response,
            username=username, email=email)

    elif email:
        user = User.get_user(email=email).first()
        return handle_wrong_username_email(
            user, password, password_missing_response,
            username=username, email=email)


def handle_wrong_username_email(user_object, password,
                                password_missing_response, **kwargs):

    authentication_failed = {
        "error": "Authentication Failed Incorret username/email or password"
    }
    if not user_object:
        return jsonify(authentication_failed), 401

    check_password = user_object.verify_password(password)
    if check_password:
        success = userDetailObject(user_object)
        return success if password else jsonify(password_missing_response)
    return jsonify(authentication_failed), 401


@user_app.route("/api/v1/auth/google", methods=['POST'])
def googleOAuth():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    access_token = request.json.get('id_token')
    if not access_token:
        return jsonify({"error": "id_token is required"}), 400

    try:
        user_details = id_token.verify_oauth2_token(
            access_token, requests.Request())

        email = user_details.get('email')
        username = user_details.get('name')
        user = User.get_user(email=email).first()

        return userDetailObject(user, username, email)

    except ValueError:
        return jsonify({"error": "Authentication Failed. Token is either"
                        " invalid or expired"}), 400


def randomPassword(stringLength=12):
    """Generate a random string of letters, digits and special characters """
    password_characters = string.ascii_letters +\
        string.digits + string.ascii_uppercase + '$@$!%*#?&'
    return ''.join(random.choice(
        password_characters) for i in range(stringLength))


def userDetailObject(user, username=None, email=None):
    if user:
        return jsonify({
            'email': user.email,
            'username': user.username,
            'token': f"{user.encode_auth_token(user.id)}"
        }), 200

    password = randomPassword()
    user = User(username=username, email=email, password=password)
    user.is_verified = True
    user.save()

    return jsonify({
        'email': user.email,
        'username': user.username,
        'token': f"{user.encode_auth_token(user.email)}"
    }), 201
