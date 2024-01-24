from application.database import db
from flask_security import UserMixin, RoleMixin
from flask_login import login_manager

# Setting up the roles_users table.
roles_users = db.Table('roles_users', db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class User(db.Model, UserMixin):
	# Setting up the user table
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
	# Setting up the role table.
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Lists(db.Model):
	# Setting up the lists table.
	__tablename__ = 'lists'
	list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	title = db.Column(db.String, unique=True)
	description = db.Column(db.String)
	tasks = db.relationship("Tasks")

class Tasks(db.Model):
	# Setting up the tasks table.
	__tablename__ = 'tasks'
	task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	list_id = db.Column(db.Integer, db.ForeignKey("lists.list_id"), nullable=False)
	title = db.Column(db.String, unique=True)
	content = db.Column(db.String)
	deadline = db.Column(db.String)
	complete = db.Column(db.Integer)
	create_date = db.Column(db.String)
	create_time = db.Column(db.String)
	update_date = db.Column(db.String)
	update_time = db.Column(db.String)
	complete_date = db.Column(db.String)
	complete_time = db.Column(db.String)
	
