from app.models import db, Recipe, environment, SCHEMA
from sqlalchemy.sql import text

from datetime import datetime, timezone

# Convert the ISO string to a datetime object with timezone
created_at_time = datetime.fromisoformat("2024-12-16T10:00:00+00:00").astimezone(
    timezone.utc
)
updated_at_time = datetime.fromisoformat("2024-12-16T10:00:00+00:00").astimezone(
    timezone.utc
)


# Adds demo recipes
def seed_recipes():
    recipe1 = Recipe(
        id=1,
        name="Dad's Smash Burger",
        yield_servings=4,
        prep_time=15,
        cook_time=10,
        total_time=25,
        short_description="Juicy gourmet burgers.",
        cuisine="American",
        difficulty="Medium",
        description="A delicious gourmet burger served with crispy hand-cut fries.",
        ingredients="Beef patties, lettuce, tomato, cheese, burger buns, fries",
        instructions="Grill the beef patties, toast the buns, assemble the burger with cheese, lettuce, and tomato.",
        tags="burger, gourmet, American",
        owner_id=1,
        visibility="Public",
        created_at=created_at_time,
        updated_at=created_at_time,
        number_likes=15,
    )

    recipe2 = Recipe(
        id=2,
        name="Veggie Stir-Fry",
        yield_servings=2,
        prep_time=10,
        cook_time=15,
        total_time=25,
        short_description="A healthy and flavorful stir-fry with mixed veggies.",
        cuisine="Asian",
        difficulty="Easy",
        description="Stir-fried mixed vegetables in a savory sauce served over rice.",
        ingredients="Broccoli, bell peppers, carrots, soy sauce, sesame oil, rice",
        instructions="Stir-fry the vegetables in sesame oil, add soy sauce, and serve over rice.",
        tags="vegetarian, stir-fry, healthy",
        image_url="https://example.com/images/veggie-stirfry.jpg",
        owner_id=2,
        visibility="Public",
        created_at=created_at_time,
        updated_at=created_at_time,
        number_likes=8,
    )

    recipe3 = Recipe(
        id=3,
        name="Chicken Alfredo",
        yield_servings=4,
        prep_time=15,
        cook_time=20,
        total_time=35,
        short_description="Creamy chicken alfredo pasta.",
        cuisine="Italian",
        difficulty="Medium",
        description="A rich and creamy chicken alfredo pasta, perfect for a comforting dinner.",
        ingredients="Chicken breast, fettuccine pasta, heavy cream, parmesan cheese, garlic, butter",
        instructions="Cook the fettuccine pasta. In a pan, cook chicken breast, then make the alfredo sauce with butter, garlic, and cream. Combine pasta and sauce.",
        tags="pasta, creamy, chicken, Italian",
        owner_id=3,
        visibility="Public",
        created_at=created_at_time,
        updated_at=created_at_time,
        number_likes=20,
    )

    recipe4 = Recipe(
        id=4,
        name="Avocado Toast",
        yield_servings=2,
        prep_time=5,
        cook_time=5,
        total_time=10,
        short_description="Simple and delicious avocado toast.",
        cuisine="American",
        difficulty="Easy",
        description="Creamy avocado spread on toasted bread, topped with a poached egg.",
        ingredients="Avocado, bread, egg, olive oil, lemon juice, salt, pepper",
        instructions="Toast the bread. Mash the avocado with olive oil, lemon juice, salt, and pepper. Spread on toast and top with a poached egg.",
        tags="breakfast, healthy, avocado, easy",
        owner_id=4,
        visibility="Public",
        created_at=created_at_time,
        updated_at=created_at_time,
        number_likes=25,
    )

    # Add the recipes to the session
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.add(recipe3)
    db.session.add(recipe4)

    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built-in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities. With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_recipes():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.recipes RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM recipes"))

    db.session.commit()
