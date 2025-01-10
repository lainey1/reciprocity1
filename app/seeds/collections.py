from app.models import db, Collection, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

# Seed data for collections
def seed_collections():
    collection1 = Collection(
        id=1,
        name="Family Favorites",
        description="A collection of recipes passed down through generations.",
        user_id=1,  # Assuming user with ID 1
        visibility="Public",  # Assuming collections are public by default
        created_at=datetime(2024, 12, 10, 9, 0, 0),
        updated_at=datetime(2024, 12, 10, 9, 0, 0)
    )

    collection2 = Collection(
        id=2,
        name="Quick & Easy",
        description="Recipes for busy weeknights, easy to prepare and delicious.",
        user_id=1,  # Assuming user with ID 1
        visibility="Public",
        created_at=datetime(2024, 12, 12, 8, 30, 0),
        updated_at=datetime(2024, 12, 12, 8, 30, 0)
    )

    collection3 = Collection(
        id=3,
        name="Comfort Food",
        description="A collection of warm and hearty recipes for cozy nights.",
        user_id=2,  # Assuming user with ID 2
        visibility="Public",
        created_at=datetime(2024, 12, 14, 9, 0, 0),
        updated_at=datetime(2024, 12, 14, 9, 0, 0)
    )

    collection4 = Collection(
        id=4,
        name="Quick Breakfasts",
        description="Quick and easy breakfast recipes to kickstart your day.",
        user_id=2,  # Assuming user with ID 2
        visibility="Public",
        created_at=datetime(2024, 12, 15, 10, 0, 0),
        updated_at=datetime(2024, 12, 15, 10, 0, 0)
    )

    db.session.add(collection1)
    db.session.add(collection2)
    db.session.add(collection3)
    db.session.add(collection4)
    db.session.commit()

def undo_collections():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.collections RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM collections"))
    db.session.commit()
