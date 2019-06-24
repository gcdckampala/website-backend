from flask import Blueprint, jsonify, request, json
from flask_user import roles_required, login_required
import requests
from .models import Roles, RolesSchema
from api.users.models import User
from api.utils.helpers import decode_auth_token, get_token


roles_app = Blueprint('roles_app', __name__)


@roles_app.route("/api/v1/roles", methods=['POST', 'GET'])
# @login_required
# @roles_required("admin")
def roles():
    role_schema = RolesSchema()
    if request.method == "GET":
        return handle_get_roles(role_schema)
    else:
        return handle_logged_in_user(role_schema)
        

def handle_logged_in_user(role_schema):
    token = get_token(http_request=request)
    user = decode_auth_token(token)
    if token and user:
        return handle_post_roles(role_schema)
    return jsonify({"error": "Authorization Header with Bearer token missing!"}), 400

def handle_get_roles(role_schema):
    
    roles = Roles.query.all()
    roles = role_schema.dump(roles, many=True).data if roles else roles
    response = {"message": "Roles fetched succesfully!", "roles": role_schema.dump(roles).data}
    return (jsonify(response), 200) if roles \
        else (jsonify({"message": "No roles added yet!"}), 404)

def handle_post_roles(role_schema):
    
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    title = request.json.get('title')
    description = request.json.get('description')

    try:
        role = Roles(title=title, description=description)
        role.save()
        return jsonify({'message': "Role successfully added!",
                        "role": role_schema.dump(role).data}), 201
    except AssertionError as exception_message:
        return jsonify(error=f"{exception_message}."), 400


