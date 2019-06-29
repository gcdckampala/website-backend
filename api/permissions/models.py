from api.utils.database import db , ma
from marshmallow import Schema
from api.utils.base import BaseModel


# association table between users and permissions
user_permissions = db.Table(
    "user_permissions",
    db.Column(
        'permissions_id',
        db.Integer(),
        db.ForeignKey('permissions.id'),
        primary_key=True),
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('users.id'),
        primary_key=True))

# Permissions model
class Permissions(BaseModel):
    __tablename__ = 'permissions'

    type = db.Column(db.String(60), nullable=False, unique=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
    users = db.relationship("User", secondary=user_permissions)


    def to_rep(self):
        return {
            "id": self.id,
            "type": self.type,
            "role_id": self.role_id
        }


class PermissionsSchema(Schema):
    class Meta:
        model = Permissions
        fields = ('id', 'type', 'role_id')