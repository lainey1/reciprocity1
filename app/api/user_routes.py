from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, User
from app.forms import UpdateUserForm, DeleteUserForm

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
    return user.to_dict()

@user_routes.route('/<int:user_id>', methods=['PUT'])
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
        return jsonify({'message': 'Only the profile owner can edit'}), 403


    # if profile owner, create instance of UserProfileForm class
    form = UpdateUserForm()

    # manually sets the CSRF token in the form from the request's cookies.
    form['csrf_token'].data = request.cookies['csrf_token']

    # if form is valid, commit data details
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.location = form.location.data
        user.bio = form.bio.data
        user.profile_image_url = form.profile_image_url.data

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


@user_routes.route('/delete_profile', methods=["GET", "POST"])
@login_required
def delete_profile():
    """
    Delete the user's profile by user ID.
    """
    form = DeleteUserForm()

    # manually sets the CSRF token in the form from the request's cookies.
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        print("Delete action triggered")  # Debugging output
        if form.delete.data:
            # Get the current user
            user_to_delete = User.query.get(current_user.id)


            # Delete the user from the database
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()

                # return redirect(url_for('home'))  ##when available Redirect to home or login page after deletion

        # elif form.cancel.data:
        #     ## when available Redirect to the user's profile page if they cancel the deletion
        #     return redirect(url_for('users.user', id=current_user.id))

    # print("Form errors:", form.errors)  # Debugging output
    return render_template("delete_profile.html", form=form)
