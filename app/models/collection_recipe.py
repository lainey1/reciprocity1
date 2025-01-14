# app/models/collection_recipe.py
from datetime import datetime

from .db import db, environment, SCHEMA, add_prefix_for_prod


class CollectionRecipe(db.Model):
    __tablename__ = 'collection_recipes'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('collections.id')), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('recipes.id')), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships

    def to_dict(self):
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'recipe_id': self.recipe_id,
            'added_at': self.added_at.isoformat() if self.added_at else None
        }
