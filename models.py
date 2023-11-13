"""Models for Your App"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create SQLAlchemy and Bcrypt instances
db = SQLAlchemy()
bcrypt = Bcrypt()

# Define a default user image URL
DEFAULT_USER_IMAGE_URL = "https://www.example.com/default-user-image.png"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False, default=DEFAULT_USER_IMAGE_URL)

    favorites = db.relationship("FavoriteList", backref="user", cascade="all, delete-orphan")
    adopted_pets = db.relationship("Adopter", backref="user", cascade="all, delete-orphan")
    given_pets = db.relationship("Giver", backref="user", cascade="all, delete-orphan")
    waitlisted_pets = db.relationship("Waitlist", backref="user", cascade="all, delete-orphan")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def signup(cls, name, email, password):
        """Sign up user.

        Hashes password and adds user to the database.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_pwd)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password`.

        This is a class method (call it on the class, not an individual user).
        It searches for a user whose email matches the provided email
        and, if it finds such a user, checks if the password matches.

        If a matching user is found and the password is correct, returns that user object.
        If no matching user is found or if the password is wrong, returns None.
        """
        user = cls.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return None

class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    breed = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    favorited_by = db.relationship("FavoriteList", backref="pet", cascade="all, delete-orphan")
    adopters = db.relationship("Adopter", backref="pet", cascade="all, delete-orphan")
    givers = db.relationship("Giver", backref="pet", cascade="all, delete-orphan")
    waitlisted_by = db.relationship("Waitlist", backref="pet", cascade="all, delete-orphan")

class FavoriteList(db.Model):
    __tablename__ = "favorite_lists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)

class Adopter(db.Model):
    __tablename__ = "adopters"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)

class Giver(db.Model):
    __tablename__ = "givers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)

class Waitlist(db.Model):
    __tablename__ = "waitlists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)

def connect_db(app):

    db.app = app
    db.init_app(app)