# //models/user.py
from datetime import datetime, timezone

from .db import db, environment, SCHEMA
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .connection import Connection


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # DEBUGGED: Define relationships with explicit foreign_keys
    connections = db.relationship(
        'Connection',
        cascade="all, delete-orphan", # FIX: remember to use delete-orphon
        foreign_keys='Connection.user_id',  # FIX: Specify the foreign key to avoid parent/child confusion
        back_populates='user',
        lazy=True
    )

    connected_users = db.relationship(
        'Connection',
        foreign_keys='Connection.connected_user_id',  # FIX: Specify the foreign key to avoid parent/child confusion
        cascade="all, delete-orphan", # FIX: Specify the foreign key to avoid parent/child confusion
        back_populates='connected_user',
        lazy=True
    )

    collection_images = db.relationship(
        'CollectionImage',
        foreign_keys='CollectionImage.user_id',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    collection_recipes = db.relationship(
        'CollectionRecipe',
        foreign_keys='CollectionRecipe.owner_id',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    collection = db.relationship(
        'Collection',
        cascade="all, delete-orphan",
        foreign_keys='Collection.user_id',
        backref='user',
        lazy=True
    )

    recipe = db.relationship(
        'Recipe',
        cascade="all, delete-orphan",
        foreign_keys="Recipe.owner_id",
        backref="user",
        lazy=True
    )

    recipe_images = db.relationship(
        'RecipeImage',
        foreign_keys='RecipeImage.user_id',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )


    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'bio': self.bio,
            'profile_image_url': self.profile_image_url,
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
