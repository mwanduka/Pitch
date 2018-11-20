from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique = True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    pitch = db.relationship('Pitch', backref='author', lazy='dynamic')
    bio = db.Column(db.String(255))
    profile_pic = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

# class Role(db.Model):
#     __tablename__ = 'roles'

#     id = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(255))
#     users = db.relationship('User',backref = 'role',lazy="dynamic")

#     def __repr__(self):
#         return f'User {self.name}'

class Pitch(db.Model):
    __tablename__ = 'pitch'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    category = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_pitch(self):
        '''
        Function that saves pitches
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_pitches(cls):
        '''
        Function that queries the databse and returns all the pitches
        '''
        return Pitch.query.all()

    @classmethod
    def get_pitches_by_category(cls,category_id):
        '''
        Function that queries the databse and returns pitches based on the
        category
        '''
        return Pitch.query.filter_by(category_id= category_id)

# class Category(db.Model):
#     '''
#     Function that defines different categories of pitches
#     '''
#     __tablename__ ='categories'


#     id = db.Column(db.Integer, primary_key=True)
#     name_of_category = db.Column(db.String(255))
#     category_description = db.Column(db.String(255))

#     @classmethod
#     def get_categories(cls):
#         '''
#         This function fetches all the categories from the database
#         '''
#         categories = PitchCategory.query.all()
#         return categories


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment= db.Column(db.String)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    username =  db.Column(db.String)
    votes= db.Column(db.Integer)

    def save_comment(self):
        '''
        Function that saves comments
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()

        return comments
