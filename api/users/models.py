from api.utils.database import DatabaseUitls, db
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import config

SECRET_KEY = config.Config.SECRET_KEY

pwd_context = CryptContext(schemes=["sha256_crypt"])


class User(db.Model, DatabaseUitls):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)

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
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e
