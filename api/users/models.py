from api.utils.database import DatabaseUitls, db, ma
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import validates
import jwt
import re
import config

SECRET_KEY = config.Config.SECRET_KEY

pwd_context = CryptContext(schemes=["pbkdf2_sha512"])


class User(db.Model, DatabaseUitls):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String())
    is_verified = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.validate_password(password)

    @classmethod
    def get_user(cls, email=None, username=None):
        if email and username:
            user = cls.query.filter_by(email=email, username=username)
        elif email and not username:
            user = cls.query.filter_by(email=email)
        elif username and not email:
            user = cls.query.filter_by(username=username)
        return user

    def __repr__(self):
        return f"<User: {self.username} {self.email}>"

    def hash_password(self, password):
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
            return token.decode('utf-8')

        except Exception as e:
            return e

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('No username provided')

        if self.get_user(username=username).first():
            raise AssertionError('Username is already in use')

        if len(username) < 5 or len(username) > 20:
            raise AssertionError(
                'Username must be between 5 and 20 characters')

        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')

        if self.get_user(email=email).first():
            raise AssertionError('Email is already in use')

        if not re.compile("[^@]+@[^@]+\.[^@]+").search(email):
            raise AssertionError('Provided email is not a valid email address')

        return email

    def validate_password(self, password):
        if not password:
            raise AssertionError('Password not provided')
        if not re.compile(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        ).search(password):
            raise AssertionError(
                "Password should have Minimum of eight characters, "
                "at least one letter, one number and one special character")

        return self.hash_password(password)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
