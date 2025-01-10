from flask import Blueprint, request

from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required

from app.forms import LoginForm
from app.forms import SignUpForm
from app.models import User, db
from ..models import Collection

auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized'}}, 401


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        user = User.query.filter(User.email == form.data['email']).first()
        login_user(user)
        return user.to_dict()
    return form.errors, 401


@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password']
        )
        db.session.add(user)
        db.session.commit()
        # Log the user in
        login_user(user)

        # Create a default family
        family_collection = Collection(
            name="FamilyRecipes",
            description="A collection of family recipes and memories.",
            user_id=user.id,
            created_at = datetime.now(datetime.timezone.utc),
            updated_at = datetime.now(datetime.timezone.utc)
        )

        db.session.add(family_collection)
        db.session.commit()

        # Return the user data and collection data
        return {
             **user.to_dict(), # ** syntax is used to unpack a dictionary
             "family_collection": family_collection.to_dict()
        }


        # return user.to_dict() ## without the family collection
    return form.errors, 401


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401
