# app/models/recipe_image.py
from datetime import datetime, timezone

from .db import db, environment, SCHEMA, add_prefix_for_prod


class RecipeImage(db.Model):
    __tablename__ = 'recipe_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('recipes.id')), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    is_preview = db.Column(db.Boolean, default=False, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationship

    def to_dict(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'user_id': self.recipe_id,
            'image_url': self.image_url,
            'caption': self.caption,
            'is_preview': self.is_preview,
            'uploaded_at': self.uploaded_at.isoformat()
        }
