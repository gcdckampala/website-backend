"""Module to seed users table"""

# Models
from api.users.models import User

data = [
    {
        "username": "admin",
        "email": "cedriclusiba@gmail.com",
        "password": "Cedric@25",
        "role_id": 1
    }
]

def seed_users():
    """Seeds sample Users
    """
    User.bulk_create(data)
