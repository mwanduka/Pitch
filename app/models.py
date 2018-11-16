# File for models/classes
from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))

    def__repr__(self):
    return f'User {self.username}'
