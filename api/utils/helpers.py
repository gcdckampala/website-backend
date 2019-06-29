#Third party
from flask import request, Blueprint, jsonify
import jwt
from config import Config


jwt_errors = {
    'NO_BEARER_MSG':
    "Bad request. The token should begin with the word\
'Bearer'.",
    'NO_TOKEN_MSG':
    "Bad request. Header does not contain an authorization\
token."
}


def get_token(http_request=request):
    """Get token from request object

    Args:
        http_request (HTTPRequest): Http request object

    Returns:
        token (string): Token string

    Raises:
        ValidationError: Validation error raised when there is no token
                         or bearer keyword in authorization header
    """
    token = http_request.headers.get('Authorization')
    if not token:
        raise ValidationError({'message': jwt_errors['NO_TOKEN_MSG']}, 401)
    elif 'bearer' not in token.lower():
        raise ValidationError({'message': jwt_errors['NO_BEARER_MSG']}, 401)
    token = token.split(' ')[-1]
    return token


def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    from api.users.models import User
    try:
        payload = jwt.decode(auth_token, Config.SECRET_KEY)
        # is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        # if is_blacklisted_token:
        #     return 'Token blacklisted. Please log in again.'
        # else:
        msg = {"error": "Invalid Token! Please login to continue."}
        user = User.get_user(email=payload['sub'])
        return user if user else (jsonify(msg), 403) 
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Signature expired. Please log in again.'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token. Please log in again.'}), 403

class ValidationError(Exception):
    """Base Validation class for handling validation errors"""

    def __init__(self, error, status_code=None):
        Exception.__init__(self)
        self.status_code = 400
        self.error = error
        self.error['status'] = 'error'
        self.error['message'] = error['message']

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return self.error