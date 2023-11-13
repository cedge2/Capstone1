from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_debugtoolbar import DebugToolbarExtension
import os
import requests
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///pawtner_up_adoptions"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
logging.basicConfig(level=logging.DEBUG)

# Importing models after app is defined
from models import db, User, connect_db


# Function to connect to the database
def connect_db(app):
    """Connect the database to our Flask app."""
    db.app = app
    db.init_app(app)

connect_db(app)

# Set up debug toolbar
debug = DebugToolbarExtension(app)

# Define PetFinder API credentials
client_id = os.environ.get('PETFINDER_CLIENT_ID')
client_secret = os.environ.get('PETFINDER_CLIENT_SECRET')
# Define PetFinder API base URL
API_BASE_URL = 'https://api.petfinder.com/v2'

# Function to get an access token

def get_token():
    global ACCESS_TOKEN, EXPIRES_IN
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    if EXPIRES_IN is None or EXPIRES_IN <= datetime.now():
        try:
            res = requests.post(
                f'{API_BASE_URL}/oauth2/token',
                headers=headers,  # Including headers in the request
                data={
                    'grant_type': 'client_credentials',
                    'client_id': client_id,
                    'client_secret': client_secret
                }
            )
            res.raise_for_status()
        except requests.HTTPError as e:
            logging.error(f"HTTP Error occurred: {e}")
            logging.error(f"Response Body: {res.text}")  # Log the response body from the API
            raise Exception(f"Failed to retrieve access token from Petfinder API: {e}")

        try:
            data = res.json()
        except ValueError as e:
            logging.error(f"Error decoding JSON: {e}")
            raise Exception("Failed to decode JSON from Petfinder API response")

        if 'access_token' not in data or 'expires_in' not in data:
            logging.error(f"Missing expected keys in response: {data}")
            raise Exception("Response from Petfinder API is missing expected keys")

        ACCESS_TOKEN = data['access_token']
        EXPIRES_IN = datetime.now() + timedelta(seconds=data['expires_in'])

    return ACCESS_TOKEN


# Initialize global variables for the access token
ACCESS_TOKEN = None
EXPIRES_IN = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pets')
def pets():
    # Call get_token to ensure ACCESS_TOKEN is up to date
    get_token()  # This function will update the ACCESS_TOKEN global variable if needed

    # Now use the ACCESS_TOKEN directly from the global scope
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{API_BASE_URL}/animals", headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        pets = response.json()['animals']
        return render_template('pets.html', pets=pets)
    else:
        flash('Could not load pets from the API.', 'danger')
        return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect('/register')
        # Use generate_password_hash to hash the password before storing it
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful.', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect('/')

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('profile.html', user=user)
    else:
        flash('Please log in to access this page.', 'danger')  # Corrected by adding the closing parenthesis and the flash category
        return redirect('/login')
