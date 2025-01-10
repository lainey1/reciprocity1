from flask.cli import AppGroup
from .users import seed_users, undo_users
from .connections import seed_connections, undo_connections
from .collections import seed_collections, undo_collections
from .recipes import seed_recipes, undo_recipes
from .recipe_images import seed_recipe_images, undo_recipe_images


from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_users()
        undo_connections()
        undo_recipes()
        undo_collections()
        undo_recipe_images()
    seed_users()
    seed_connections()
    seed_recipes()
    seed_collections()
    seed_recipe_images()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    undo_connections()
    undo_recipes()
    undo_collections()
    undo_recipe_images()
    # Add other undo functions here
