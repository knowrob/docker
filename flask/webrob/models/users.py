
from flask_user import UserMixin
from webrob.app_and_db import db

# Define the User-Roles pivot table
user_roles = db.Table('user_roles',
    db.Column('id', db.Integer(), primary_key=True),
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    displayname = db.Column(db.String(50), nullable=False, default='')
    remoteapp = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, default='')
    reset_password_token = db.Column(db.String(100), nullable=False, default='')
    api_token = db.Column(db.String(64), nullable=False, default='')
    container_id = db.Column(db.String(255), nullable=False, default='')

    # Relationships
    roles = db.relationship('Role', secondary=user_roles,
            backref=db.backref('users', lazy='dynamic'))
    
    def first_role(self):
        if len(self.roles)==0: return None
        else: return self.roles[0].name
