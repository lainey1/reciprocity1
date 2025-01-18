from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

# from app.forms import ImageForm
from app.models import CollectionImage, Collection, db

collection_images_routes = Blueprint('collection_images', __name__)


@collection_images_routes.route('/', methods=["GET"])
def all_images():
    """
    Query for all collection image and return as image dictionary.
    """

    try:
        images = CollectionImage.query.all()
        return {'collection_images': [image.to_dict() for image in images]}

    except SQLAlchemyError as e:
        # Database debugging line
        current_app.logger.error(f"Database query error: {str(e)}")
        return jsonify({
            'message': 'An error occurred while fetching recipes. Please try again later.'
        }), 500

    except Exception as e:
        # Server debugging line
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500


@collection_images_routes.route('/collection/<int:collection_id>', methods=['GET'])
@login_required
def get_collection_image(collection_id):
    """
    Query and return collection image for a specific collection.
    """
    collection = Collection.query.get(collection_id)
    # print("COLLECTION ========>", collection)

    # Validate collection existence
    if not collection:
        return jsonify({"error": "Collection not found"}), 404

    collection_images = CollectionImage.query.filter_by(collection_id=collection_id).all()

    if not collection_images:
        return jsonify({"message": "No image found for this collection"}), 404

    # Serialize the collection images
    collection_images_data = [
        {
            "id": image.id,
            "collection_id": image.collection_id,
            "image_url": image.image_url,
        }
        for image in collection_images
    ]

    return jsonify({
        "collection_id": collection_id,
        "collection_images": collection_images_data
    }), 200


@collection_images_routes.route('/collection/<int:collection_id>', methods=['PUT'])
@login_required
def replace_collection_image(collection_id):
    """
    Replace the image for a specific collection (only by the collection owner).
    """
    try:
        # Fetch the collection by ID
        collection = Collection.query.get(collection_id)
        print(collection)

        # Validate collection existence
        if not collection:
            return jsonify({"message": "Collection not found"}), 404

        # Log ownership validation
        print(f"Collection owner ID: {collection.user_id}, Current user ID: {current_user.id}")

        # Validate ownership
        if collection.user_id != current_user.id:
            return jsonify({
                "message": "You are not authorized to update this collection's image. Only the collection owner can perform this action."
            }), 403

        # Parse the JSON payload
        payload = request.json
        print(f"Payload received: {payload}")

        # Validate required field
        if 'image_url' not in payload or not payload['image_url']:
            return jsonify({
                "message": "Missing required field: 'image_url'."
            }), 400

        # Fetch or create a new CollectionImage for the collection
        collection_image = CollectionImage.query.filter_by(collection_id=collection_id).first()

        if not collection_image:
            current_app.logger.debug("No existing image found. Creating a new image.")
            collection_image = CollectionImage(
                collection_id=collection_id,
                image_url=payload['image_url']
            )
            db.session.add(collection_image)
        else:
            current_app.logger.debug(f"Updating existing image with ID: {collection_image.id}")
            collection_image.image_url = payload['image_url']

        # Save changes
        db.session.commit()
        current_app.logger.debug(f"Image updated successfully for collection ID: {collection_id}")

        return jsonify({
            "message": "Collection image updated successfully!",
            "collection_image": collection_image.to_dict()
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error while replacing collection image: {str(e)}")
        return jsonify({
            "message": "An error occurred while updating the collection image. Please try again later."
        }), 500

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error while replacing collection image: {str(e)}")
        return jsonify({
            "message": "An unexpected error occurred. Please try again later.",
            "error": str(e)
        }), 500


@collection_images_routes.route('/collection/<int:collection_id>', methods=['DELETE'])
@login_required
def delete_collection_image(collection_id):
    """
    Delete the image for a specific collection (only by the collection owner).
    """
    # Fetch the collection by ID
    collection = Collection.query.get(collection_id)

    # Validate collection existence
    if not collection:
        return jsonify({"message": "Collection not found"}), 404

    # Validate ownership
    if collection.user_id != current_user.id:
        return jsonify({
            "message": "You are not authorized to delete this collection's image. Only the collection owner can perform this action."
        }), 403

    try:
        # Fetch the existing CollectionImage for the collection
        collection_image = CollectionImage.query.filter_by(collection_id=collection_id).first()

        if not collection_image:
            return jsonify({"message": "No image found for this collection."}), 404

        # Delete the image
        db.session.delete(collection_image)
        db.session.commit()

        return jsonify({"message": "Collection image deleted successfully!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error while deleting collection image: {str(e)}")
        return jsonify({
            "message": "An error occurred while deleting the collection image. Please try again later."
        }), 500

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error while deleting collection image: {str(e)}")
        return jsonify({
            "message": "An unexpected error occurred. Please try again later.",
            "error": str(e)
        }), 500
