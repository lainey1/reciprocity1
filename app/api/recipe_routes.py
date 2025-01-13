from flask import Blueprint, jsonify, current_app, request, json
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app.models import db, Recipe, RecipeImage, User
from app.forms import CreateRecipeForm, IngredientForm, InstructionForm
from datetime import datetime


recipe_routes = Blueprint('recipes', __name__)

@recipe_routes.route('/new', methods=["POST"])
@login_required
def add_recipe():
    """Route to add a new recipe."""
    payload = request.json
    form = CreateRecipeForm()
    form['csrf_token'].data = request.cookies.get('csrf_token', '')

    # Manually assign form data
    form.name.data = payload.get('name')
    form.yield_servings.data = payload.get('yield_servings')
    form.prep_time.data = payload.get('prep_time')
    form.cook_time.data = payload.get('cook_time')
    form.total_time.data = payload.get('total_time')
    form.cuisine.data = payload.get('cuisine')
    form.short_description.data = payload.get('short_description')
    form.description.data = payload.get('description')
    form.tags.data = payload.get('tags')
    form.visibility.data = payload.get('visibility')

    # Clear and populate dynamic fields
    form.ingredients.entries.clear()
    for ingredient in payload.get('ingredients', []):
        form.ingredients.append_entry({'ingredient': ingredient.get('ingredient', '').strip()})

    form.instructions.entries.clear()
    for instruction in payload.get('instructions', []):
        form.instructions.append_entry({'instruction': instruction.get('instruction', '').strip()})

    if form.validate():
        ingredients_json = json.dumps([{"ingredient": field.ingredient.data} for field in form.ingredients])
        instructions_json = json.dumps([{"instruction": field.instruction.data} for field in form.instructions])
        tags_string = ','.join([tag.strip() for tag in form.tags.data.split(",")])

        new_recipe = Recipe(
            name=form.name.data,
            owner_id=current_user.id,
            yield_servings=form.yield_servings.data,
            prep_time=form.prep_time.data,
            cook_time=form.cook_time.data,
            total_time=form.total_time.data,
            cuisine=form.cuisine.data,
            short_description=form.short_description.data,
            description=form.description.data,
            tags=tags_string,
            ingredients=ingredients_json,  # Store as JSON string
            instructions=instructions_json,  # Store as JSON string
            visibility=form.visibility.data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_recipe)
        db.session.commit()

        return jsonify({"message": "Recipe created successfully!", "recipe": new_recipe.to_dict()}), 201

    return jsonify({"message": "Invalid form data", "errors": form.errors}), 400

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
