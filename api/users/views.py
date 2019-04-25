from flask import Blueprint, jsonify, request
from .models import User

user_app = Blueprint('user_app', __name__)


@user_app.route("/api/v1/auth/signup", methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None or email is None:
        return jsonify({'error': 'all fields are required'}), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'user already exists'}), 400
    user = User(username=username, email=email, password=password)
    user.save()
    return jsonify({'username': user.username}), 201
