"""Module to seed role table"""

# Models
from api.roles.models import Roles

data = [
    {
        "title": "admin",
        "description": "admin user can do anything"
    },
    {
        "title": "Regular user",
        "description": "Regular user"
    },
    {
        "title": "mentor",
        "description": "In charge of mentoring subscribers"
    }
]

def seed_roles():
    """Seeds sample Roles
    """
    Roles.bulk_create(data)

    
