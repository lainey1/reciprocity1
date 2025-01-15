# app/models/recipe_image.py
from datetime import datetime, timezone

from .db import db, environment, SCHEMA, add_prefix_for_prod


class CollectionImage(db.Model):
    __tablename__ = 'collection_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('collections.id')), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    image_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationship

    def to_dict(self):
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'user_id': self.user_id,
            'image_url': self.image_url,
            'caption': self.caption,
            'uploaded_at': self.uploaded_at.isoformat()
        }
