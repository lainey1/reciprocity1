from flask.cli import AppGroup
from .users import seed_users, undo_users
from .connections import seed_connections, undo_connections
from .collections import seed_collections, undo_collections
from .recipes import seed_recipes, undo_recipes
from .recipe_images import seed_recipe_images, undo_recipe_images
from .collection_recipes import seed_collection_recipes, undo_collection_recipes
from .collection_images import seed_collection_images, undo_collection_images


from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')

# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        undo_users()
        undo_connections()
        undo_recipes()
        undo_collections()
        undo_recipe_images()
        undo_collection_recipes()
        undo_collection_images()
    seed_users()
    seed_connections()
    seed_recipes()
    seed_collections()
    seed_recipe_images()
    seed_collection_recipes()
    seed_collection_images()



# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    undo_connections()
    undo_recipes()
    undo_collections()
    undo_recipe_images()
    undo_collection_recipes()
    undo_collection_images()
