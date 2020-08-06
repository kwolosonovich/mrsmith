'''SQLAlchemy models'''

from flask import session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    '''Users model.'''
    
    __tablename__ = 'users'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    username = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )
    
    email = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )
    
    password = db.Column(
        db.String,
        nullable=False,
    )
    
    likes = db.relationship(
        'Image',
        secondary="likes"
    )
    

    @classmethod
    def create(cls, username, email, password):
        '''Register a new user and hash password'''
        
        hashed = bcrypt.generate_password_hash(password)
        hashed_password = hashed.decode("utf8")
        user = cls(
            username=username,
            email=email,
            password=hashed_password,
        )
        db.session.add(user)
        session['CURR_USER'] = user.username
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Valid username and password."""
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        
    def user_login(username):
        """Log in user."""
        session['CURR_USER'] = username
        return True
    
    def verify_login():
        """Validate if user is logged in."""
        if 'CURR_USER' in session:
            return True
        else:
            return False
    
    
class Image(db.Model):
    '''Images model'''

    __tablename__= 'images'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    url = db.Column(
        db.String
    )
    
    title = db.Column(
        db.String 
    )
    
    artist = db.Column (
        db.String
    )
    
    date = db.Column(
        db.String
    )
    
    collection = db.Column(
        db.Text
    )
    

class Like(db.Model):
    '''User likes for images model.'''

    __tablename__ = 'likes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', 
                      ondelete='CASCADE'
                      )
    )

    image_id = db.Column(
        db.Integer,
        db.ForeignKey('images.id', 
                    #   ondelete='CASCADE'
                      )
    )
    
    # future tasks

# class Follow(db.Model):
#     '''User following boards model.'''

#     __tablename__ = 'follows'

#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id',
#                       #   ondelete='CASCADE'
#                       )
#     )

#     board_id = db.Column(
#         db.Integer,
#         db.ForeignKey('images.id'
#                       #   ondelete='CASCADE'
#                       )
    # )
    
    
# class Board(db.Model):
#     '''User board model.'''

#     __tablename__= 'boards'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         # cascade='all, delete-orphan'
#     )

#     user_id = db.Column(
#         db.Integer,
#         # db.ForeignKey('users.id', cascade="all, delete-orphan")
#         db.ForeignKey('users.id')
#     )

#     name = db.Column(
#         db.String
#     )
    
# '''Boards and images table'''
# board_images = db.Table('board_images', 
#                         db.Column('boards.id', 
#                                   db.Integer, 
#                                   db.ForeignKey('boards.id'), 
#                                   primary_key=True),
#                         db.Column('images.id',
#                                 db.Integer,
#                                 db.ForeignKey('images.id'),
#                                 primary_key=True)
#                         )
 

def connect_db(app):
    '''Connect database to Flask app.'''

    db.app = app
    db.init_app(app)


