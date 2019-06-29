"""Module to seed permissions table"""

# Models
from api.permissions.models import Permissions

data = [
    {
        "type": "create events",
        "role_id": 1
    },
    {
        "type": "block user",
        "role_id": 1
    },
    {
        "type": "view learner details",
        "role_id": 3
    }
]

def seed_permissions():
    """Seeds sample Permissions
    """
    Permissions.bulk_create(data)
