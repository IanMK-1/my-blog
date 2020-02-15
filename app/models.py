from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_manager
from datetime import datetime


class Writer(db.Model):
    __tablename__ = 'writers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    writer_password = db.Column(db.String(255))

    # return a printable representation of the object
    def __repr__(self):
        return f'Writer{self.full_name}'

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.writer_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.writer_password, password)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    user_password = db.Column(db.String(255))

    # return a printable representation of the object
    def __repr__(self):
        return f'User{self.username}'

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)