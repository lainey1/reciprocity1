from flask import Blueprint, current_app, jsonify
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

# from app.forms import ImageForm
from app.models import RecipeImage, Recipe

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

@recipe_images_routes.route('/recipe/<int:recipe_id>/images', methods=['POST'])
@login_required
def upload_image(recipe_id):
    """
    Handle image upload for a specific recipe.
    """
    recipe = Recipe.query.get(recipe_id)

    # Validate recipe existence
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    # Handle POST request to upload images
    form = ImageForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    # Validate form submission
    if not form.validate_on_submit():
        return jsonify({"error": "Invalid form submission", "errors": form.errors}), 400

    # Check for image data
    image_url = form.image_url.data
    is_preview = form.is_preview.data

    if not image_url:
        return jsonify({"error": "No image uploaded"}), 400

    # Process and save images
    try:
        if not image_url.startswith(('http://', 'https://')):
            return jsonify({"error": f"Invalid URL: {image_url}"}), 400

        restaurant_image = RecipeImage(
            recipe_id=recipe.id,
            user_id=current_user.id,
            url=image_url,
            is_preview=is_preview
        )

        db.session.add(restaurant_image)
        db.session.commit()

        return jsonify({"message": "Image uploaded successfully", "image": restaurant_image.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error saving images: {str(e)}"}), 500



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
