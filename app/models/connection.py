# app/models/connection.py
from datetime import datetime, timezone

from .db import db, environment, SCHEMA, add_prefix_for_prod


class Connection(db.Model):
    __tablename__ = 'connections'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    connected_user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    connection_type = db.Column(db.String(20), nullable=False)  # 'Family' or 'Friend'
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationships



    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'connected_user_id': self.connected_user_id,
            'connection_type': self.connection_type,
            'created_at': self.created_at.isoformat()
        }
