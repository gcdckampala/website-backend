from flask import Blueprint, jsonify, request
from .models import User
import jwt


user_app = Blueprint('user_app', __name__)


@user_app.route("/api/v1/auth/signup", methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    username_email_present = check_username_email(username, email)
    
    if not username_email_present  and User.get_user(username=username).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=username, email=email, password=password)
    user.save()
    return jsonify({'username': user.username}), 201

def check_username_email(username, email):
    if not username or  not email:
        entity = "username" if not username else "email" 
        return jsonify({'error': f'{entity} field is required.'}), 400

@user_app.route("/api/v1/auth/login", methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    both_fields_missing = not username and not email
    both_fields_present = username and email
    three_fields_present = both_fields_present and password
    password_missing = not password
    email_missing = not email and username
    username_missing = not username and email

    password_missing_response = {'error': 'Password is required for login.'}

    if both_fields_present or three_fields_present:
        return jsonify({"msg": "Please use either username or email to login but not both!"})

    else:
        return handle_response(both_fields_missing, password_missing,
                               email_missing, username_missing, username,
                               email, password, password_missing_response)

def login_helper(*args):
    email_missing, username_missing, username, email, password, password_missing_response = args
    if email_missing:
        user = User.get_user(username=username).first()
        return handle_wrong_username_email(user,password, password_missing_response, username=username, email=email)


    elif username_missing:
        user = User.get_user(email=email).first()
        return handle_wrong_username_email(user,password, password_missing_response, username=username, email=email)
        


def handle_wrong_username_email(user_object, password, password_missing_response, **kwargs):
    
    if not user_object:
        response = {"error": "Please enter the correct {}".format(entity_name(kwargs))} 
        return jsonify(response)

    check_password = user_object.verify_password(password)
    if check_password:
        token = user_object.encode_auth_token(user_object.id)
        success = {
            "msg": f"User {user_object.username} successfully logged in!",
            "token": token.decode()
        }
        return jsonify(success) if password else jsonify(password_missing_response)
    return jsonify({"error": "Please enter correct password!"})


def entity_name(args_dict):
    username, email = args_dict.get('username'), args_dict.get('email')
    if username:
        return "username"
    elif email:
        return "email"

def handle_response(*args):
    both_fields_missing, password_missing, email_missing, username_missing, username, email, password, password_missing_response = args
    if both_fields_missing:
        all_fields_missing_response = {'error': 'Login fields can not be empty.'}
        email_username_missing_response = {'error': 'Either email or username field is required for login.'}
        return (jsonify(all_fields_missing_response), 400) if password_missing else (jsonify(email_username_missing_response), 400)
    else:
        return login_helper(email_missing, username_missing, username, email, password, password_missing_response)
