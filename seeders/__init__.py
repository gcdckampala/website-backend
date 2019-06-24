""" Module for seeding sample data into the database """

# Standard library
from collections import OrderedDict

# Third party
from sqlalchemy import text



# Local Imports
from .seed_user_roles import seed_roles
from .seed_user_permissions import seed_permissions
from .seed_users import seed_users

# Database
from api.utils.database import db



SEED_OPTIONS = ('users', 'roles', 'permissions', 'spaces')


def seed_db(entity_name=None):
    """Checks the argument provided and matches it to the respective seeder

    Args:
        resource_name (str): Name of resource

    Return:
        func: calls a function with the resource name as arguments
    """

    entity_order_mapping = OrderedDict({
        'roles':
        seed_roles,
        'permissions':
        seed_permissions,
        'users':
        seed_users
    })

    if entity_name:
        return entity_order_mapping.get(entity_name)()

    else:
        for entity_seed_func in entity_order_mapping.values():
            entity_seed_func()
