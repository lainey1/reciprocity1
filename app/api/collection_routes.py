from datetime import datetime, timezone

from flask import Blueprint, current_app, json, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app.models import Collection, User, db

collection_routes = Blueprint('collections', __name__)


@collection_routes.route('/', methods=["GET"])
def collections():
    """
    Query to get all collections and return them in a list of collection dictionaries.
    """

    try:
        # Fetch all collections
        collections = Collection.query.all()

        # If no collections found, return an empty list with a success message
        if not collections:
            return jsonify({
                'message': 'No collections found',
                'collections': []
            }), 200

        # Make an empty list to store all collections
        all_collections_list = []

        # Go through each collection
        for collection in collections:

            # Convert single collection to a dictionary
            collection_dictionary = collection.to_dict()

            # Safely handle optional fields, defaulting to None or empty values
            collection_dictionary['description'] = collection_dictionary.get('description') or ''

            # Fetch owner information
            owner = User.query.get(collection.user_id)
            if owner:
                collection_dictionary['owner'] = owner.username  # Or any other field from the User model

            # Append the collection dictionary to the all collections list
            all_collections_list.append(collection_dictionary)

        # Return the data as JSON
        return jsonify({
            'collections': all_collections_list
        }), 200

    except SQLAlchemyError as e:
        # Log the error for debugging purposes
        current_app.logger.error(f"Database query error: {str(e)}")
        return jsonify({
            'message': 'An error occurred while fetching collections. Please try again later.'
        }), 500

    except Exception as e:
        # Catch any other unexpected errors
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500


@collection_routes.route('/<int:id>', methods=['GET'])
def get_collection_by_id(id):
    """
    Get a single collection by its ID.
    """

    try:
        # Fetch the collection by ID
        collection = Collection.query.get(id)

        # Check if collection exists
        if not collection:
            return jsonify({
                'message': f'Collection with ID {id} not found.'
            }), 404

        # Convert collection to dictionary
        collection_data = collection.to_dict()

        # Fetch owner information
        owner = User.query.get(collection.user_id)
        if owner:
            collection_data['owner'] = owner.username

        # Return the collection data as JSON
        return jsonify({
            'collection': collection_data
        }), 200

    except SQLAlchemyError as e:
        # Log and handle database-related errors
        current_app.logger.error(f"Database query error: {str(e)}")
        return jsonify({
            'message': 'An error occurred while fetching the collection. Please try again later.'
        }), 500

    except Exception as e:
        # Handle unexpected errors
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500


@collection_routes.route('/owner/<int:owner_id>', methods=['GET'])
def collections_by_owner(owner_id):
    """Query to get all collections by owner id and return them as a list of collection dictionaries"""

    try:
        # Fetch all collections owned by the user
        collections_by_owner = Collection.query.filter_by(user_id=owner_id).all()

        # If no collections found, return a message indicating no collections
        if not collections_by_owner:
            return jsonify({
                'message': 'No collections found for this owner.'
            }), 404

        # Make an empty list to store owner's collections
        owners_collections_list = []

        # Go through each collection
        for collection in collections_by_owner:
            # Convert to single collection in dictionary
            collection_data = collection.to_dict()


            # Append the collection dictionary to the owner's collections list
            owners_collections_list.append(collection_data)

            # Return the data as JSON
        return jsonify({
            'recipes_owned_by_user': owners_collections_list
        }), 200

    except SQLAlchemyError as e:
        # debugging log
        current_app.logger.error(f"Database query error: {str(e)}")
        return jsonify({
            {'message': 'An error occurred while fetching collections. Please try again later.'}
        }), 500

    except Exception as e:
        # Catch any other unexpected errors
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500


@collection_routes.route('/new', methods=["POST"])
@login_required
def add_collection():
    """Route to add a new collection."""

    try:
        payload = request.json

        # Validate required fields are in the payload
        required_fields = ["name","visibility"]
        missing_fields = [field for field in required_fields if field not in payload or not payload[field]]
        if missing_fields:
            return jsonify({
                "message": "Missing required fields.",
                "missing_fields": missing_fields
            }), 400


        # Get current time and use datetime object
        now = datetime.now(timezone.utc)

        new_collection = Collection(
            name=payload.get("name"),
            user_id=current_user.id,
            description=payload.get("description"),
            visibility=payload.get("visibility"),
            created_at=now,  # Pass datetime object directly
            updated_at=now   # Pass datetime object directly
        )

        print(f"Attempting to add collection with name ==========> {new_collection}")

        try:
            db.session.add(new_collection)
            db.session.commit()
            print(f"Successfully added collection with ID: {new_collection.id}")
        except Exception as e:
            print(f"Failed to add collection {new_collection.name}: {str(e)}")
            db.session.rollback()
            raise

        return jsonify({
            "message": "Collection created successfully!",
            "collection": new_collection.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback changes if error occurs
        print(f"Error in /new route: {e}")  # Log the error
        return jsonify({
            "message": "Failed to create collection",
            "error": str(e)
        }), 500


@collection_routes.route('/<int:collection_id>/edit', methods=["PUT"])
@login_required
def update_collection(collection_id):
    """Route to update a collection by ID."""

    # Fetch collection by ID
    collection = Collection.query.get(collection_id)

    if not collection:
        return jsonify({'message': 'Collection not found'}), 404

    # Check if the current user is the collection's owner
    if collection.user_id != current_user.id:
        return jsonify({'message': 'You are not authorized to update this collection. Please log in as the owner.'}), 403

    # Get data from request
    try:
        data = request.get_json()

        # Validate required fields are in the payload
        required_fields = ["name", "visibility"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                "message": "Missing required fields.",
                "missing_fields": missing_fields
            }), 400

        # Update collection using form data
        collection.name = data['name']
        collection.description = data.get('description', collection.description)  # Use existing value if not provided
        collection.visibility = data['visibility']

        # Save changes to the database
        db.session.commit()

    except Exception as e:
        print(f"Error in /<int:collection_id>/edit route: {e}")
        return jsonify({'message': 'An error occurred while updating the collection.'}), 500

    return jsonify({
        "message": "Collection updated successfully!",
        "collection": collection.to_dict()
    }), 200


@collection_routes.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    """ Delete a collection by ID from the database. """
    collection = Collection.query.get(id)

    if not collection:
        return {'error': f'Collection with ID {id} not found.'}, 404

    if request.method == 'DELETE':
        # Check if the current user is the owner of the restaurant
        if collection.user_id != current_user.id:
            return {'error': 'You are not authorized to delete this collection.'}, 403

        db.session.delete(collection)
        db.session.commit()
        return {'message': f'Collection with ID {id} deleted successfully.'}, 200
