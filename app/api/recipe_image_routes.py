from datetime import datetime, timezone

from flask import Blueprint, current_app, json, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

# from app.forms import ImageForm
from app.models import Recipe, RecipeImage, db

recipe_images_routes = Blueprint('recipe_images', __name__)


@recipe_images_routes.route('/', methods=["GET"])
def all_images():
    """
    Query for all recipe images and return them in a list of image dictionaries.
    """

    try:
        recipe_images = RecipeImage.query.all()
        return {'recipe_images': [image.to_dict() for image in recipe_images]}

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


@recipe_images_routes.route('/recipes/<int:recipe_id>', methods=['GET'])
@login_required
def get_recipe_images(recipe_id):
    """
    Query and return all images for a specific recipe.
    """
    recipe = Recipe.query.get(recipe_id)

    # Validate recipe existence
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    recipe_images = RecipeImage.query.filter_by(recipe_id=recipe_id).all()

    if not recipe_images:
        return jsonify({"message": "No images found for this recipe"}), 404

    return jsonify({
        "recipe_id": recipe_id,
        "recipe_images": [image.to_dict() for image in recipe_images]  # Include image data (with ID)
    }), 200


@recipe_images_routes.route('/recipe/<int:recipe_id>', methods=['POST'])
@login_required
def add_recipe_image(recipe_id):
    """
    Route to add new recipe image.
    - User must be logged in and owner.
    """
    # Fetch recipe by ID
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({'message': 'Recipe not found'}), 404

    try:
        payload = request.json

        # Check if the current user is the recipe's owner
        if recipe.owner_id != current_user.id:
            return jsonify({'message': 'You are not authorized to update this recipe. Please log in as the owner.'})

        # Validate required fields are in the payload
        required_fields = ["image_url"]
        missing_fields = [field for field in required_fields if field not in payload or not payload[field]]
        if missing_fields:
            return jsonify({
                "message": "Missing required fields.",
                "missing_fields": missing_fields
            }), 400

        # Get current time and use datetime object
        now = datetime.now(timezone.utc)

        new_recipe_image = RecipeImage(
            image_url=payload.get("image_url"),
            recipe_id=recipe_id,
            user_id=current_user.id,
            caption=payload.get("caption"),
            is_preview=payload.get("is_preview"),
            uploaded_at=now,  # Pass datetime object directly
        )

        print(f"Attempting to add recipe image url: {new_recipe_image.image_url} to {recipe.name}")

        try:
            db.session.add(new_recipe_image)
            db.session.commit()
            print(f"Successfully added recipe image with ID: {new_recipe_image.id}")
        except Exception as e:
            print(f"Failed to add recipe {new_recipe_image.name}: {str(e)}")
            db.session.rollback()
            raise

        return jsonify({
            "message": "Recipe image created successfully!",
            "recipe": new_recipe_image.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback changes if error occurs
        print(f"Error in /new route: {e}")  # Log the error
        return jsonify({
            "message": "Failed to create recipe image",
            "error": str(e)
        }), 500


@recipe_images_routes.route('/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    """
    Delete a recipe image by ID
    """
    image = RecipeImage.query.filter_by(id=image_id).first()

    if image:
        # Ensure the user is the one who created the image or is the owner of the recipe
        if image.user_id != current_user.id:
            return {'message': 'You are not authorized to delete this image.'}, 403

        db.session.delete(image)
        db.session.commit()

        return {'message': 'Image deleted successfully'}

    return {'error': 'Image not found.'}, 404



@recipe_images_routes.route('/<int:image_id>', methods=['PUT'])
@login_required
def update_image(image_id):
    """
    Update a recipe image by ID
    """
    image = RecipeImage.query.filter_by(id=image_id).first()

    if not image:
        return jsonify({"error": "Image not found"}), 404

    # Ensure the user is the one who created the image or is the owner of the recipe
    if image.user_id != current_user.id or image.recipe.owner_id != current_user.id:
        return jsonify({'message': 'You are not authorized to update this image.'}), 403

    form = ImageForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission", "errors": form.errors}), 400

    image_url = form.image_url.data
    is_preview = form.is_preview.data

    if image_url and not image_url.startswith(('http://', 'https://')):
        return jsonify({"error": f"Invalid URL: {image_url}"}), 400

    try:
        # Update the image attributes
        if image_url:
            image.url = image_url
        if is_preview is not None:
            image.is_preview = is_preview

        db.session.commit()
        return jsonify({"message": "Image updated successfully", "image": image.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error updating image: {str(e)}"}), 500
