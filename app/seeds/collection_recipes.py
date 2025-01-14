from app.models import db, Collection, Recipe, CollectionRecipe, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

# Seed data for collections
def seed_collections():
    collection_recipe1 = CollectionRecipe(
        id=1,
        collection_id=1,
        recipe_id=1,
        owner_id=1,  # Remy
        visibility="Everyone",
        created_at=datetime(2025, 12, 10, 9, 0, 0),
    )

    collection_recipe2 =
    CollectionRecipe(
        id=2,
        collection_id=5,
        recipe_id=2,
        owner_id=1,  # Remy
        visibility="Everyone",
        created_at=datetime(2025, 1, 10, 9, 0, 0),
        updated_at=datetime(2025, 12, 10, 9, 0, 0)

    )


    collection_recipe2 = Collection(
        id=2,
        name="Family Recipes",
        description="A collection of family recipes and memories.",
        user_id=2,  # Alfredo
        visibility="Everyone",
        created_at=datetime(2024, 12, 11, 8, 30, 0),
        updated_at=datetime(2024, 12, 11, 8, 30, 0)
    )

    family_collection3 = Collection(
        id=3,
        name="Family Recipes",
        description="A collection of family recipes and memories.",
        user_id=3,  # Colette
        visibility="Everyone",
        created_at=datetime(2024, 12, 12, 9, 0, 0),
        updated_at=datetime(2024, 12, 12, 9, 0, 0)
    )

    family_collection4 = Collection(
        id=4,
        name="Family Recipes",
        description="A collection of family recipes and memories.",
        user_id=4,  # Lainey
        visibility="Everyone",
        created_at=datetime(2024, 12, 13, 10, 0, 0),
        updated_at=datetime(2024, 12, 13, 10, 0, 0)
    )

    quick_n_easy = Collection(
        id=5,
        name="Quick & Easy",
        description="Recipes for busy weeknights, easy to prepare and delicious.",
        user_id=1,  # Remy
        visibility="Everyone",
        created_at=datetime(2024, 12, 12, 8, 30, 0),
        updated_at=datetime(2024, 12, 12, 8, 30, 0)
    )

    comfort_food = Collection(
        id=6,
        name="Comfort Food",
        description="A collection of warm and hearty recipes for cozy nights.",
        user_id=2,  # Alfredo
        visibility="Everyone",
        created_at=datetime(2024, 12, 14, 9, 0, 0),
        updated_at=datetime(2024, 12, 14, 9, 0, 0)
    )

    quick_breakfast = Collection(
        id=7,
        name="Quick Breakfasts",
        description="Quick and easy breakfast recipes to kickstart your day.",
        user_id=2,  # Alfredo
        visibility="Everyone",
        created_at=datetime(2024, 12, 15, 10, 0, 0),
        updated_at=datetime(2024, 12, 15, 10, 0, 0)
    )

    db.session.add(collection_recipe1)
    db.session.add(collection_recipe2)
    db.session.add(collection_recipe3)
    db.session.add(collection_recipe4)
    db.session.add(collection_recipe5)
    db.session.add(collection_recipe6)
    db.session.add(collection_recipe7)
    db.session.commit()

def undo_collections():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.collections RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM collections"))
    db.session.commit()
