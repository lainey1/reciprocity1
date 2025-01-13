from flask import Blueprint, request, jsonify

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash


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

    # Ensure CSRF token is included for validation
    form['csrf_token'].data = request.cookies.get('csrf_token')

    # Check if the form is valid
    if not form.validate():
        # Collect all validation error messages
        errors = {field: error[0] for field, error in form.errors.items()}
        return jsonify({
            "message": "Invalid Request",
            "errors": errors
        }), 400

    # Perform user authentication
    user = User.query.filter(
        (User.email == form.data['email_or_username']) |
        (User.username == form.data['email_or_username'])
    ).first()

    if user and check_password_hash(user.password, form.data['password']):
        login_user(user)
        return user.to_dict()

    # Return invalid credentials error if user not authenticated
    return {'errors': {'message': 'Invalid Request'}}, 401


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

     # Check if the form is valid
    if not form.validate():
        # Collect all validation error messages
        errors = {field: error[0] for field, error in form.errors.items()}
        return jsonify({
            "message": "Invalid Request",
            "errors": errors
        }), 400

    if form.validate_on_submit():
        user = User(
            first_name=form.data['first_name'],
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
        )

        db.session.add(family_collection)
        db.session.commit()

        # Return the user data and collection data
        return {
             **user.to_dict(), # ** syntax is used to unpack a dictionary
             "family_collection": family_collection.to_dict()
        }


        # return user.to_dict() ## without the family collection
     # Return invalid credentials error if user not authenticated
    return form.errors, 401


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401
