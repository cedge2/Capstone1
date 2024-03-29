from flask import Flask, redirect, render_template, request, flash, redirect, session, g
import json
from datetime import datetime, timedelta
from flask_cors import CORS
import os
import requests, random
import flask
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, FavoritePet, FavoriteOrg, FavPetComment, OrgComment
from forms import UserForm, LoginForm, UserPreferenceForm, CommentForm



app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
API_KEY=os.environ.get('API_KEY') 
API_SECRET=os.environ.get('API_SECRET') 
DemoUsername=os.environ.get('DemoUsername') 
DemoPassword=os.environ.get('DemoPassword') 

API_BASE_URL = 'https://api.petfinder.com/v2'
ACCESS_TOKEN = None
EXPIRES_IN = None
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
CURR_USER_KEY = 'curr_user'

def get_token():
    global ACCESS_TOKEN 
    global EXPIRES_IN
    global headers 
    if EXPIRES_IN is None or EXPIRES_IN <= datetime.now() :
        
        res = requests.post(f'{API_BASE_URL}/oauth2/token', 
                            data={
                                'grant_type':'client_credentials', 
                                'client_id': API_KEY, 
                                'client_secret': API_SECRET})
        data=res.json()
        ACCESS_TOKEN = data['access_token']
        EXPIRES_IN = datetime.now() + timedelta(seconds=data['expires_in'])
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    print(ACCESS_TOKEN)


@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None 

def do_login(user):
    session[CURR_USER_KEY] = user.id

def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



#routes

@app.route('/signup', methods=["GET", "POST"])
def signup():
    do_logout()
    form = UserForm()
    if form.validate_on_submit():
        try:
            user =User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()
            do_login(user)
            return redirect('/questions')  
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)     
    else:
        return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
     
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )
        if user:
            do_login(user)
            return redirect("/questions")
        else:
            flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    do_logout()

    flash('You have logged out successfully', 'success')
    return redirect('/home')

@app.route('/users/profile/<int:user_id>', methods=['GET', 'POST'])
def show_edit_user(user_id):

    if not g.user or g.user.id != user_id:
        flash('Please log in')
        return redirect('/login')
    
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.updateUser(form.username.data, form.email.data, form.password.data)

        db.session.commit()

        flash('Your Info was Successfully Updated!', 'success')

        return render_template('user_profile.html', form = form, user=user)
    
    return render_template('user_profile.html', form = form, user=user)

@app.route('/questions', methods=["GET", "POST"])
def show_questions():
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/home")    
    
    form = UserPreferenceForm()

    if form.validate_on_submit():
        try:
            get_token()
            response = requests.get(f'{API_BASE_URL}/animals', 
                                    headers=headers, 
                                    params={
                                        'type': form.pet_type.data, 
                                        'size': form.size.data, 
                                        'gender': form.gender.data, 
                                        'age': form.age.data, 
                                        'location': form.zipcode.data, 
                                        'limit': 100, 
                                        'status': 'adoptable',
                                        'distance': 20})
            match_data = response.json()
            list_of_animals = match_data['animals']
        except KeyError:
            print(f"no animal found {response}")
            flash('No Match Found. Please Try Again.', 'danger')
            return redirect('/questions')

        user = User.query.get_or_404(g.user.id)  
        
        for animal in list_of_animals:
            if len(animal['photos']) == 0:
                list_of_animals.remove(animal)
            if(animal['id'] in [pet.pet_id for pet in user.favorite_pets]):
                list_of_animals.remove(animal)
        
        if len(list_of_animals) == 0 :
            flash('No Match Found. Please Try Again.', 'danger')
            return redirect('/questions')
        elif len(list_of_animals) > 10:
            list_of_animals= random.sample(list_of_animals, 10)
            return render_template('match_result.html', list_of_animals=list_of_animals)
        elif len(list_of_animals) > 0:       
            return render_template('match_result.html', list_of_animals=list_of_animals)

    return render_template('questions.html', form=form)

@app.route("/")
def root():
    return redirect('/home')

@app.route('/home')
def home():

    if g.user:
        return redirect('/questions')
    return render_template('home.html')

@app.route('/likes', methods=['POST'])
def add_fav():
  
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/home")
    
    received_data=request.get_json()
    return_data = {
        'status':'success',
        'message': f'received:{received_data["animal"]}'
    }

    user = User.query.get_or_404(g.user.id)
    favorites = user.favorite_pets
    if FavoritePet.query.filter_by(pet_id=received_data['animal']).first() in favorites:
        return_data = {
        'status':'already in database',
        'message': f'received:{received_data["animal"]}'
        }
        return flask.Response(response=json.dumps(return_data), status=201)
    else:
        favPet = FavoritePet(
        pet_id = received_data['animal'],
        user_id = g.user.id)

        db.session.add(favPet)
        db.session.commit()

        return flask.Response(response=json.dumps(return_data), status=201)

@app.route('/org-search', methods=['GET'])
def show_search_page():
   
    return render_template('org_search.html')


@app.route('/comments/<int:pet_id>', methods=['POST'])
def add_pet_comments(pet_id):
  
    received_data=request.get_json()
    return_data = {
        'status':'successful',
        'message': f'received:pet_id {received_data["animal"]}, comment:{received_data["comment"]}'
    }

    favorite_pet = FavoritePet.query.filter(FavoritePet.pet_id == pet_id, FavoritePet.user_id == g.user.id).one()
    
    comment = FavPetComment(
        user_id=g.user.id,
        fav_pet_id=favorite_pet.id,
        comment=received_data['comment']
    )

    db.session.add(comment)
    db.session.commit()

    return flask.Response(response=json.dumps(return_data), status=201)


@app.route('/org-results', methods=['GET'])
def org_search_result():
   
    get_token()

    user_query = request.args.get('q')
    response = requests.get(f'{API_BASE_URL}/organizations', headers=headers, params={'query': user_query})
    data = response.json()
    orgs = data['organizations']
    
    return render_template('org_results.html', user_query=user_query, orgs_list=orgs)
    
    
@app.route('/delete-fav', methods=['DELETE'])
def delete_fav():
  
    received_data=request.get_json()
    print(f'received:{received_data}')
    return_data = {
        'status':'successfully deleted',
        'message': f'received:{received_data}'
    }

    FavoritePet.query.filter(FavoritePet.pet_id == received_data['animal'], FavoritePet.user_id == g.user.id).delete()
    db.session.commit()

    return flask.Response(response=json.dumps(return_data), status=201)


@app.route('/pets/users/<int:user_id>')
def user_page(user_id):

    if not g.user or g.user.id != user_id:
        flash('Please log in', "danger")
        return redirect('/home')
    
    get_token()

    form=CommentForm()

    user = User.query.get_or_404(user_id)
    favorites=user.favorite_pets
    fav_pets_id = [pet.pet_id for pet in favorites]
    fav_pets =[]    

    for pet_id in fav_pets_id:
        try:
            response = requests.get(f'{API_BASE_URL}/animals/{pet_id}', headers=headers)
            data = response.json()
            fav_pets.append(data['animal'])

        except KeyError:
            FavoritePet.query.filter_by(pet_id = pet_id).delete()
            db.session.commit()

    comments = FavPetComment.query.filter_by(user_id = g.user.id)

    return render_template('users_pets.html', user=user, fav_pets=fav_pets, comments = comments, form=form)



