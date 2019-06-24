from flask import Blueprint, jsonify, request, json
from flask_user import roles_required, login_required
import requests
from .models import Permissions, PermissionsSchema
from api.users.models import User
from api.utils.helpers import decode_auth_token, get_token


permissions_app = Blueprint('permissions_app', __name__)


@permissions_app.route("/api/v1/permissions", methods=['POST', 'GET'])
# @login_required
# @roles_required("admin")
def permissions():
    permission_schema = PermissionsSchema()
    if request.method == "GET":
        return handle_get(permission_schema)
    else:
        return handle_logged_in_user(permission_schema)        

def handle_logged_in_user(permission_schema):
    token = get_token(http_request=request)
    user = decode_auth_token(token)
    if token and user:
        return handle_post(permission_schema)
    return jsonify({"error": "Authorization Header with Bearer token missing!"}), 400

    

def handle_get(permission_schema):
    permissions = Permissions.query.all()
    permissions = permission_schema.dump(permissions, many=True).data if permissions else permissions
    response = {"message": "Permissions fetched succesfully!", "permissions": permissions}
    return (jsonify(response), 200) if permissions \
        else (jsonify({"message": "No permissions added yet!"}), 404)

def handle_post(permission_schema):
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    type_ = request.json.get('type')
    role_id = request.json.get('role_id')

    try:
        permission = Permissions(type=type_, role_id=role_id)
        permission.save()
        return jsonify({'message': "Permission successfully added!",
                        "role": permission.type}), 201
    except AssertionError as exception_message:
        return jsonify(error=f"{exception_message}."), 400

