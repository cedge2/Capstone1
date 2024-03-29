from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class FavoriteOrg(db.Model):
    __tablename__ ='favorite_orgs'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable = False
    )
    org_id = db.Column(
        db.Text,
        nullable=False
    )
    user = db.relationship('User', backref='favorite_orgs')
    def __repr__(self):
        return f'<FavOrg #{self.id} user:{self.user_id}, org_id:{self.org_id} >'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(25),
        nullable=False,
        unique=True,
    )
    password = db.Column(
        db.Text,
        nullable=False,
    )
    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    def __repr__(self):
        return f'<User #{self.id}, {self.username}, {self.email}>'
    def updateUser(self, username, email, password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.username = username
        self.email=email
        self.password =hashed_pwd
        return f'user: updated'

    @classmethod
    def signup(cls, username, email, password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False
    
class FavPetComment(db.Model):
    __tablename__ ='fav_pet_comments'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable= False
    )  
    fav_pet_id = db.Column(
        db.Integer,
        db.ForeignKey('favorite_pets.id', ondelete='cascade'),
        nullable= False
    )  
    comment= db.Column(
        db.Text
    )
    user = db.relationship('User', backref='comments')
    fav_pet = db.relationship('FavoritePet', backref='comments')
    def __repr__(self):
        return f'<FavPetComments #{self.id} user:{self.user_id}, pet_id:{self.fav_pet_id} comment:{self.comment}>'

class FavoritePet(db.Model):
    __tablename__ ='favorite_pets'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable = False
    ) 
    pet_id = db.Column(
        db.Integer,
        nullable=False
    )
    user = db.relationship('User', backref='favorite_pets')

    def __repr__(self):
        return f'<FavPets #{self.id} user:{self.user_id} pet_id:{self.pet_id} >'

class OrgComment(db.Model):
    __tablename__ ='org_comments'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable= False
    )    
    org_id = db.Column(
        db.Text
    )
    comment= db.Column(
        db.Text
    )
    user = db.relationship('User', backref='org_comments')
    def __repr__(self):
        return f'<OrgComments #{self.id} user:{self.user_id}, org_id:{self.org_id} comment:{self.comment}>'
    

    

