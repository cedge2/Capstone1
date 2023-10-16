from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet, Candidate, AdoptionStatus
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt_pet"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = ""

toolbar = DebugToolbarExtension(app)

PETFINDER_API_URL = "https://api.petfinder.com/v2/"
PETFINDER_API_KEY = ""

connect_db(app)
db.create_all()

@app.route("/")
def root():

    response = requests.get(f"{PETFINDER_API_URL}animals", headers={"Authorization": f"Bearer {PETFINDER_API_KEY}"})
    pets = response.json().get("animals", [])
    return render_template("pets/homepage.html", pets=pets)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/candidates")
def candidates_index():
    candidates = Candidate.query.all()
    return render_template("candidates/index.html", candidates=candidates)

@app.route("/candidates/<int:candidate_id>")
def candidates_show(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    return render_template("candidates/show.html", candidate=candidate)

@app.route("/pets/<int:pet_id>")
def pets_show(pet_id):
    response = requests.get(f"{PETFINDER_API_URL}animals/{pet_id}", headers={"Authorization": f"Bearer {PETFINDER_API_KEY}"})
    pet = response.json().get("animal")
    return render_template("pets/show.html", pet=pet)

@app.route("/pets/<int:pet_id>/adopt", methods=["POST"])
def adopt_pet(pet_id):
    candidate_id = request.form["candidate_id"]
    adoption_status = AdoptionStatus(pet_id=pet_id, candidate_id=candidate_id, status="Pending")
    db.session.add(adoption_status)
    db.session.commit()
    flash(f"Adoption request submitted for pet {pet_id}.")
    return redirect("/")

@app.route("/candidates/<int:candidate_id>")
def candidates_show(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    return render_template("candidates/show.html", candidate=candidate)

@app.route("/pets/<int:pet_id>")
def pets_show(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template("pets/show.html", pet=pet)

@app.route("/pets/<int:pet_id>/adopt", methods=["POST"])
def adopt_pet(pet_id):
    candidate_id = request.form["candidate_id"]
    adoption_status = AdoptionStatus(pet_id=pet_id, candidate_id=candidate_id, status="Pending")
    db.session.add(adoption_status)
    db.session.commit()
    flash(f"Adoption request submitted for pet {pet_id}.")
    return redirect("/pets")

@app.route("/adoption-requests")
def adoption_requests():
    adoption_requests = AdoptionStatus.query.all()
    return render_template("adoption-requests/index.html", adoption_requests=adoption_requests)

@app.route("/adoption-requests/<int:request_id>/approve", methods=["POST"])
def approve_adoption_request(request_id):
    if not session.get("is_admin"):
        abort(403)
    adoption_request = AdoptionStatus.query.get_or_404(request_id)
    adoption_request.status = "Approved"
    db.session.commit()
    flash(f"Adoption request for pet {adoption_request.pet_id} approved.", "success")
    return redirect("/adoption-requests")

@app.route("/adoption-requests/<int:request_id>/cancel", methods=["POST"])
def cancel_adoption_request(request_id):
    if not session.get("is_admin"):
        abort(403)
    adoption_request = AdoptionStatus.query.get_or_404(request_id)
    adoption_request.status = "Canceled"
    db.session.commit()
    flash(f"Adoption request for pet {adoption_request.pet_id} canceled.", "danger")
    return redirect("/adoption-requests")

