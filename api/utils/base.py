from .database import db
from datetime import datetime


class DatabaseUitls:
    
    def save(self):
        '''Utility method for saving new objects'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''Utility method for deleting objects'''
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def bulk_create(cls, raw_list):
        """
        Save raw list of records to database

        Parameters:
            raw_list(list): List of records to be saved to database
        """
        resource_list = [cls(**item) for item in raw_list]
        db.session.add_all(resource_list)
        db.session.commit()

class BaseModel(db.Model, DatabaseUitls):
    """ Base model for all database models.

    attributes:
        id (string, reserved):
             a unique identifier for each instance. Autogenerated.
        deleted (bool, required):
            a flag for soft deletion of model instances.
    """

    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    deleted = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)