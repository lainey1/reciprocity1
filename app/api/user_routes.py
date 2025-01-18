from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required

from app.forms import DeleteUserForm, UpdateUserForm
from app.models import User, db

user_routes = Blueprint('users', __name__)


@user_routes.route('/')
@login_required
def users():
    """
    Query for all users and returns them in a list of user dictionaries
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def user(id):
    """
    Query for a user by id and returns that user in a dictionary
    """
    user = User.query.get(id)
    return {'user': user.to_dict()}

@user_routes.route('/<int:user_id>/', methods=['PUT'])
@login_required
def update_profile(user_id):
    """
    Update user profile by id
    """

    # get the user by id
    user = User.query.get(user_id)

    # if user id does not exist, return a 404 not found error
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # if user is not the profile owner, return 403 Forbidden
    if user.id != current_user.id:
        return jsonify({
        "message": "Only the profile owner can make changes to these details."
        }
        ), 403


    if user:
        user.bio = request.json.get('bio', user.bio)
        user.location = request.json.get('location', user.location)
        user.profile_image_url = request.json.get('profile_image_url', user.profile_image_url)
        user.first_name = request.json.get('first_name', user.first_name)
        db.session.commit()
        return user.to_dict()  # Ensure this method does NOT include a nested 'user'

    # commit updated data to db and confirm success
    try:
        db.session.commit()
        return jsonify({
            'message': 'User profile updated successfully',
            'user': user.to_dict()
        }), 200

    # notify user if there was an error saving the data
    except Exception as e:
        # undo any changes made during the transaction to ensure consistency
        db.session.rollback()
        return jsonify({'message': 'Error saving the data', 'error': str(e)}),

    # if form data is not valid, notify user
    return jsonify({
        'message': 'Invalid user data',
        'errors': form.errors
    }), 400

@user_routes.route('/<int:user_id>', methods=["POST"])
@login_required
def delete_profile(user_id):
    """Delete the user's profile by user ID."""
    if user_id != current_user.id:
        return jsonify({"message": "Only the profile owner can delete their account."}), 403

    # if profile owner, create instance of DeleteProfileForm class
    form = DeleteUserForm()

    # manually sets the CSRF token in the form from the request's cookies.
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        if form.delete.data:  # If the "Delete Profile" button was pressed
            user_to_delete = User.query.get(user_id)
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
                return jsonify({'message': 'User profile deleted successfully'}), 200
                # return redirect(url_for('home'))  ##when available Redirect to home or login page after deletion
        elif form.cancel.data:  # If the "Cancel" button was pressed
            return redirect(url_for('users.user', id=current_user.id))

    return render_template("delete_profile.html", form=form)



@user_routes.route('/delete_profile', methods=["GET", "POST"])
@login_required
def get_delete_profile_form():
    """
    Delete the user's profile by user ID.
    """

    form = DeleteUserForm()

    # print("Form errors:", form.errors)  # Debugging output
    return render_template("delete_profile.html", form=form)
