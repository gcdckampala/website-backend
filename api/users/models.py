from api.utils.database import DatabaseUitls, db
from passlib.context import CryptContext

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

    def __repr__(self):
        return f"<User: {self.username} {self.email}>"

    def hash_password(self, password):
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
