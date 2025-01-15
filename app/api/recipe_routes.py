from datetime import datetime, timezone
from flask import Blueprint, jsonify, current_app, request, json
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app.models import db, Recipe, RecipeImage, User


recipe_routes = Blueprint('recipes', __name__)


@recipe_routes.route('/', methods=["GET"])
def recipes():
    """Query to get all recipes and return them in a list of recipe dictionaries."""

    try:
        # Fetch all recipes
        recipes = Recipe.query.all()

        # If no recipes found, return an empty list with a success message
        if not recipes:
            return jsonify({
                'message': 'No recipes found',
                'recipes': []
            }), 200

        # Make an empty list to store all recipes
        all_recipes_list = []

        # Go through each recipe
        for recipe in recipes:
            # Grab its preview image
            preview_image = RecipeImage.query.filter_by(recipe_id=recipe.id, is_preview=True).first()
            preview_image_url = preview_image.image_url if preview_image else None

            # Convert single recipe to a dictionary
            recipe_dictionary = recipe.to_dict()

            # Add the preview image and optional tags to the recipe dictionary
            recipe_dictionary['preview_image'] = preview_image_url

            # Safely handle optional fields, defaulting to None or empty values
            recipe_dictionary['prep_time'] = recipe_dictionary.get('prep_time') or None
            recipe_dictionary['cook_time'] = recipe_dictionary.get('cook_time') or None
            recipe_dictionary['short_description'] = recipe_dictionary.get('short_description') or ''
            recipe_dictionary['description'] = recipe_dictionary.get('description') or ''
            recipe_dictionary['tags'] = recipe_dictionary.get('tags') or []

            # Ensure the ingredients and instructions are safe for iteration (i.e., default to an empty list if None)
            recipe_dictionary['ingredients'] = json.loads(recipe.ingredients) if recipe.ingredients else []
            recipe_dictionary['instructions'] = json.loads(recipe.instructions) if recipe.instructions else []

            # Fetch owner information (assuming User model exists and has a 'username' field)
            owner = User.query.get(recipe.owner_id)
            if owner:
                recipe_dictionary['owner'] = owner.username  # Or any other field from the User model

            # Append the recipe dictionary to the all recipes list
            all_recipes_list.append(recipe_dictionary)

        # Return the data as JSON
        return jsonify({
            'recipes': all_recipes_list
        }), 200

    except SQLAlchemyError as e:
        # Log the error (for debugging purposes) and return a generic error message
        current_app.logger.error(f"Database query error: {str(e)}")
        return jsonify({
            'message': 'An error occurred while fetching recipes. Please try again later.'
        }), 500

    except Exception as e:
        # Catch any other unexpected errors
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500


@recipe_routes.route('/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    """Get a single recipe by its ID."""
    try:
        # Fetch the recipe by ID
        recipe = Recipe.query.get(id)

        # Check if recipe exists
        if not recipe:
            return jsonify({
                'message': f'Recipe with ID {id} not found.'
            }), 404

        # Convert recipe to dictionary
        recipe_data = recipe.to_dict()

        # Fetch its preview image
        preview_image = RecipeImage.query.filter_by(recipe_id=recipe.id, is_preview=True).first()
        recipe_data['preview_image'] = preview_image.image_url if preview_image else None

        # Fetch owner information
        owner = User.query.get(recipe.owner_id)
        if owner:
            recipe_data['owner'] = owner.username

        # Return the recipe data as JSON
        return jsonify({
            'recipe': recipe_data
        }), 200

    except SQLAlchemyError as e:
        # Log and handle database-related errors
        current_app.logger.error(f"Database query error: {str(e)}")
        return jsonify({
            'message': 'An error occurred while fetching the recipe. Please try again later.'
        }), 500

    except Exception as e:
        # Handle unexpected errors
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500


@recipe_routes.route('/owner/<int:owner_id>', methods=['GET'])
def recipes_by_owner(owner_id):
    """Query to get all recipes by owner id and return them as a list of recipe dictionaries"""

    try:
        # Fetch all recipes owned by the user
        recipes_by_owner = Recipe.query.filter_by(owner_id=owner_id).all()

        # If no recipes found, return a message indicating no recipes
        if not recipes_by_owner:
            return jsonify({
                'message': 'No recipes found for this owner.'
            }), 404

        # Make an empty list to store owner's recipes
        owners_recipes_list = []

        # Go through each recipe
        for recipe in recipes_by_owner:
            # Convert to single recipe in dictionary
            recipe_data = recipe.to_dict()

            # Grab its preview image
            preview_image = RecipeImage.query.filter_by(recipe_id=recipe.id, is_preview=True).first()
            preview_image_url = preview_image.image_url if preview_image else None

            # Add preview image to recipe's dictionary
            recipe_data['preview_image'] = preview_image_url

            # Append the recipe dictionary to the owner's recipes list
            owners_recipes_list.append(recipe_data)

            # Return the data as JSON
        return jsonify({
            'recipes_owned_by_user': owners_recipes_list
        }), 200

    except SQLAlchemyError as e:
        # Log the error (for debugging purposes) and return as a generic error message
        current_app.logger.error(f"Database query error: {str(e)}")
        return jsonify({
            {'message': 'An error occurred while fetching recipes. Please try again later.'}
        }), 500

    except Exception as e:
        # Catch any other unexpected errors
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500


@recipe_routes.route('/new', methods=["POST"])
@login_required
def add_recipe():
    """Route to add a new recipe."""

    try:
        payload = request.json

        # Validate required fields are in the payload
        required_fields = ["name", "yield_servings", "ingredients", "instructions", "visibility"]
        missing_fields = [field for field in required_fields if field not in payload or not payload[field]]
        if missing_fields:
            return jsonify({
                "message": "Missing required fields.",
                "missing_fields": missing_fields
            }), 400

        # Extract data from the payload
        ingredients = payload.get("ingredients", [])
        instructions = payload.get("instructions", [])
        tags = payload.get("tags", "")

        # Serialize ingredients and instructions
        ingredients_json = json.dumps([{"ingredient": ingredient} for ingredient in ingredients])
        instructions_json = json.dumps([{"instruction": instruction} for instruction in instructions])

        # Handle tags
        if isinstance(tags, str):
            tags_string = ','.join([tag.strip() for tag in tags.split(",") if tag.strip()])
        else:
            tags_string = ''

        # Get current time and use datetime object
        now = datetime.now(timezone.utc)

        new_recipe = Recipe(
            name=payload.get("name"),
            owner_id=current_user.id,
            yield_servings=payload.get("yield_servings"),
            prep_time=payload.get("prep_time"),
            cook_time=payload.get("cook_time"),
            total_time=payload.get("total_time"),
            cuisine=payload.get("cuisine"),
            short_description=payload.get("short_description"),
            description=payload.get("description"),
            tags=tags_string,
            ingredients=ingredients_json,  # Store as JSON string
            instructions=instructions_json,  # Store as JSON string
            visibility=payload.get("visibility"),
            created_at=now,  # Pass datetime object directly
            updated_at=now   # Pass datetime object directly
        )

        print(f"Attempting to add recipe with name: {new_recipe.name}")

        try:
            db.session.add(new_recipe)
            db.session.commit()
            print(f"Successfully added recipe with ID: {new_recipe.id}")
        except Exception as e:
            print(f"Failed to add recipe {new_recipe.name}: {str(e)}")
            db.session.rollback()
            raise

        return jsonify({
            "message": "Recipe created successfully!",
            "recipe": new_recipe.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback changes if error occurs
        print(f"Error in /new route: {e}")  # Log the error
        return jsonify({
            "message": "Failed to create recipe",
            "error": str(e)
        }), 500


@recipe_routes.route('/<int:recipe_id>/edit', methods=["PUT"])
@login_required
def update_recipe(recipe_id):
    """Route to update a recipe by ID."""

    # Fetch recipe by ID
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({'message': 'Recipe not found'}), 404

    # Check if the current user is the recipe's owner
    if recipe.owner_id != current_user.id:
        return jsonify({'message': 'You are not authorized to update this recipe. Please log in as the owner.'})

    # Get data from request
    try:
        data = request.get_json()
        recipe_data = data.get("recipe", {})
        print("Request data:", recipe_data)
    except Exception as e:
        print(f"Error in /<int:recipe_id>/edit route: {e}")

    # Validate required fields are in the payload
    required_fields = ["name", "yield_servings", "ingredients", "instructions", "visibility"]
    missing_fields = [field for field in required_fields if field not in recipe_data]

    if missing_fields:
        return jsonify({
            "message": "Missing required fields.",
            "missing_fields": missing_fields
        }), 400

    # Extract ingredients, instructions & tags data from the payload
    ingredients = recipe_data.get("ingredients", [])
    instructions = recipe_data.get("instructions", [])
    tags = recipe_data.get("tags", "")

    # Serialize ingredients, instructions & tags
    ingredients_json = json.dumps([{"ingredient": ingredient["ingredient"]} for ingredient in ingredients])
    instructions_json = json.dumps([{"instruction": instruction["instruction"]} for instruction in instructions])
    tags_string = ','.join([tag.strip() for tag in tags.split(",") if tag.strip()])

    # Update recipe using form data
    recipe.name = recipe_data['name']
    recipe.yield_servings = recipe_data['yield_servings']
    recipe.prep_time = recipe_data.get('prep_time', 0)
    recipe.cook_time = recipe_data.get('cook_time', 0)
    recipe.total_time = recipe_data.get('total_time', 0)
    recipe.cuisine = recipe_data.get('cuisine', "")
    recipe.short_description = recipe_data.get('short_description', "")
    recipe.description = recipe_data.get('description', "")
    recipe.tags = tags_string
    recipe.ingredients = ingredients_json  # Store as JSON string
    recipe.instructions = instructions_json  # Store as JSON string
    recipe.visibility = recipe_data['visibility']

    # Save changes to the database
    db.session.commit()

    return jsonify({
        "message": "Recipe updated successfully!",
        "recipe": recipe.to_dict()
    }), 200


@recipe_routes.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    """ Delete a recipe by ID from the database. """
    recipe = Recipe.query.get(id)

    if not recipe:
        return {'error': f'Recipe with ID {id} not found.'}, 404

    if request.method == 'DELETE':
        # Check if the current user is the owner of the restaurant
        if recipe.owner_id != current_user.id:
            return {'error': 'You are not authorized to delete this recipe.'}, 403

        db.session.delete(recipe)
        db.session.commit()
        return {'message': f'Recipe with ID {id} deleted successfully.'}, 200
