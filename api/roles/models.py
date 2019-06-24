from api.utils.database import db, ma
from marshmallow import Schema
from api.utils.base import BaseModel




# Roles model
class Roles(BaseModel):
    __tablename__ = 'roles'
    title = db.Column(db.String(60), nullable=False, unique=True)  
    description = db.Column(db.String(250), nullable=False)
    
    roles_permissions = db.relationship(
        'Permissions',
        backref='roles',
        cascade='save-update,delete',
        lazy='dynamic')

    users = db.relationship( 
        'User',
        backref='role',
        cascade='delete',
        lazy='dynamic')


    def to_rep(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }


class RolesSchema(Schema):
    class Meta:
        model = Roles
        fields = ('id', 'title', 'description')