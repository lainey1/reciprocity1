#app/models/recipe.py
import json
from datetime import datetime, timezone

from .db import db, environment, SCHEMA, add_prefix_for_prod


class Recipe(db.Model):
    __tablename__ = 'recipes'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    yield_servings = db.Column(db.Integer, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    total_time = db.Column(db.Integer, nullable=False)
    short_description = db.Column(db.String(150), nullable=True)
    cuisine = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    tags = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String, nullable=True)
    visibility = db.Column(db.String(20), nullable=False, server_default='Public')
    number_likes = db.Column(db.Integer, nullable=False, server_default='0')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    # Relationships
    # recipe_images = db.relationship('RecipeImage', backref='recipe', lazy=True)
    # recipe_pins = db.relationship('RecipePin', backref='recipe', lazy=True)
    # recipe_reviews = db.relationship('RecipeReview', backref='recipe', lazy=True)
    # recipe_collections = db.relationship('CollectionRecipe', backref='recipe', lazy=True)
    # family_recipes = db.relationship('FamilyRecipe', backref='recipe', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'yield_servings': self.yield_servings,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'total_time': self.total_time,
            'short_description': self.short_description,
            'cuisine': self.cuisine,
            'difficulty': self.difficulty,
            'description': self.description,
            'ingredients': json.loads(self.ingredients) if self.ingredients else None,
            'instructions': json.loads(self.instructions) if self.instructions else None,
            'tags': self.tags,
            'image_url': self.image_url,

            'visibility': self.visibility,
            'number_likes': self.number_likes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
