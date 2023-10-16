import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/user-login-icon-14.png"

class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    breed = db.Column(db.Text, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    location = db.Column(db.Text, nullable=True)

class AdoptionStatus(db.Model):
    __tablename__ = "adoption_statuses"

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    status = db.Column(db.Text, nullable=False, default="Pending")

    candidate = db.relationship("Candidate", backref="adoption_statuses")
    pet = db.relationship("Pet", backref="adoption_statuses")

def connect_db(app):
    db.app = app
    db.init_app(app)
