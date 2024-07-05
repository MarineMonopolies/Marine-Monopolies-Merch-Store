from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String)
    username = db.Column(db.String)
    roles = db.relationship('Role', secondary='user_roles')
    #role = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, username):
        self.email = email
        self.password = generate_password_hash(password)
        self.username = username

    def check_password(self, password):
        # We updated to Werkzeug 3.x, so we can't use MD5 anymore
        print(self.password)
        print(password)
        return check_password_hash(self.password, password)
    
    def has_roles(self, *roles):
        return any(role.name in roles for role in self.roles)

    def is_admin(self):
        return self.has_roles('admin')

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('login.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

# Define the Product data-model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    price = db.Column(db.Float())
    image = db.Column(db.String(100))
    status = db.Column(db.Integer())

    def show_status(self):
        status_map = {
            0: "Approved",
            1: "In Review",
            2: "Rejected"
        }
        return status_map[self.status]

class Announcements(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))
    author = db.Column(db.String(255))
    time = db.Column(db.DateTime())

