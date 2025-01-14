import json
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
        name="Remy's Ratatouille",
        yield_servings=4,
        prep_time=20,
        cook_time=45,
        total_time=65,
        short_description="Anton Ego approved. Long and narrow vegetables work best. Serve with crusty bread or over a bed of brown rice, couscous, or pasta.",
        cuisine="French",
        description="A visually stunning and delicious dish of layered vegetables baked in a savory tomato sauce.",
        ingredients=json.dumps([
            {"ingredient": "1 (6 ounce) can tomato paste"},
            {"ingredient": "1/2 onion, chopped"},
            {"ingredient": "1/4 cup minced garlic"},
            {"ingredient": "3/4 cup water"},
            {"ingredient": "4 tablespoons olive oil, divided"},
            {"ingredient": "Salt and ground black pepper to taste"},
            {"ingredient": "1 small eggplant, trimmed and very thinly sliced"},
            {"ingredient": "1 zucchini, trimmed and very thinly sliced"},
            {"ingredient": "1 yellow squash, trimmed and very thinly sliced"},
            {"ingredient": "1 red bell pepper, cored and very thinly sliced"},
            {"ingredient": "1 yellow bell pepper, cored and very thinly sliced"},
            {"ingredient": "1 teaspoon fresh thyme leaves, or to taste"},
            {"ingredient": "3 tablespoons mascarpone cheese"}
        ]),
        instructions=json.dumps([
            {"instruction": "Preheat the oven to 375 degrees F (190 degrees C)."},
            {"instruction": "Spread tomato paste onto the bottom of a 10-inch square baking dish."},
            {"instruction": "Sprinkle with onion and garlic."},
            {"instruction": "Stir in water and 1 tablespoon olive oil until thoroughly combined."},
            {"instruction": "Season with salt and pepper."},
            {"instruction": "Arrange alternating slices of eggplant, zucchini, yellow squash, red bell pepper, and yellow bell pepper, starting at the outer edge of the dish and working concentrically towards the center."},
            {"instruction": "Overlap slices slightly to display colors."},
            {"instruction": "Drizzle vegetables with remaining 3 tablespoons olive oil; season with salt and pepper."},
            {"instruction": "Sprinkle with thyme leaves."},
            {"instruction": "Cover vegetables with a piece of parchment paper cut to fit inside."},
            {"instruction": "Bake in the preheated oven until vegetables are roasted and tender, about 45 minutes."},
            {"instruction": "Serve with dollops of mascarpone cheese."}
        ]),
        tags="vegetarian, healthy, French, classic",
        # tags=["vegetarian", "healthy", "French", "classic"],
        owner_id=1,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
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
        description="Stir-fried mixed vegetables in a savory sauce served over rice.",
        ingredients=json.dumps([
            {"ingredient": "Broccoli"},
            {"ingredient": "bell peppers"},
            {"ingredient": "carrots"},
            {"ingredient": "soy sauce"},
            {"ingredient": "sesame oil"},
            {"ingredient": "rice"}
        ]),
        instructions=json.dumps([
            {"instruction": "Stir-fry the vegetables in sesame oil, add soy sauce, and serve over rice."}
        ]),
        tags="vegetarian, stir-fry, healthy",
        # tags=["vegetarian", "stir-fry", "healthy"],
        owner_id=2,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
    )

    recipe3 = Recipe(
        id=3,
        name="Mama's Chicken Alfredo",
        yield_servings=4,
        prep_time=15,
        cook_time=20,
        total_time=35,
        short_description="Creamy chicken alfredo pasta.",
        cuisine="Italian",
        description="A rich and creamy chicken alfredo pasta, perfect for a comforting dinner.",
        ingredients=json.dumps([
            {"ingredient": "Chicken breast"},
            {"ingredient": "fettuccine pasta"},
            {"ingredient": "heavy cream"},
            {"ingredient": "parmesan cheese"},
            {"ingredient": "garlic"},
            {"ingredient": "butter"}
        ]),
        instructions=json.dumps([
            {"instruction": "Cook the fettuccine pasta."},
            {"instruction": "In a pan, cook chicken breast, then make the alfredo sauce with butter, garlic, and cream."},
            {"instruction": "Combine pasta and sauce."}
        ]),
        tags="pasta, creamy, chicken, Italian",
        # tags=["pasta", "creamy", "chicken", "Italian"],
        owner_id=3,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
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
        description="Creamy avocado spread on toasted bread, topped with a poached egg.",
        ingredients=json.dumps([
            {"ingredient": "Avocado"},
            {"ingredient": "bread"},
            {"ingredient": "egg"},
            {"ingredient": "olive oil"},
            {"ingredient": "lemon juice"},
            {"ingredient": "salt"},
            {"ingredient": "pepper"}
        ]),
        instructions=json.dumps([
            {"instruction": "Toast the bread."},
            {"instruction": "Mash the avocado with olive oil, lemon juice, salt, and pepper."},
            {"instruction": "Spread on toast and top with a poached egg."}
        ]),
        tags="breakfast, healthy, avocado, easy",
        # tags=["breakfast", "healthy", "avocado", "easy"],
        owner_id=4,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
    )

    recipe5 = Recipe(
        id=5,
        name="Papa's Smash Burger",
        yield_servings=4,
        prep_time=15,
        cook_time=10,
        total_time=25,
        short_description="Juicy gourmet burgers.",
        cuisine="American",
        description="A delicious gourmet burger served with crispy hand-cut fries.",
        ingredients=json.dumps([
            {"ingredient": "Beef patties"},
            {"ingredient": "lettuce"},
            {"ingredient": "tomato"},
            {"ingredient": "cheese"},
            {"ingredient": "burger buns"},
            {"ingredient": "fries"}
        ]),
        instructions=json.dumps([
            {"instruction": "Grill the beef patties."},
            {"instruction": "Toast the buns."},
            {"instruction": "Assemble the burger with cheese, lettuce, and tomato."}
        ]),
        tags="burger, gourmet, American",
        # tags=["vegetarian", "healthy", "French", "classic"],
        owner_id=3,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
    )

    recipe6 = Recipe(
        id=6,
        name="Grandma's Chicken Adobo",
        yield_servings=4,
        prep_time=10,
        cook_time=45,
        total_time=55,
        short_description="A classic Filipino dish with savory, tangy flavors.",
        cuisine="Filipino",
        description="Tender chicken simmered in a flavorful mixture of soy sauce, vinegar, garlic, and spices.",
        ingredients=json.dumps([
            {"ingredient": "Chicken drumsticks or thighs"},
            {"ingredient": "soy sauce"},
            {"ingredient": "vinegar"},
            {"ingredient": "garlic"},
            {"ingredient": "bay leaves"},
            {"ingredient": "black peppercorns"},
            {"ingredient": "water"},
            {"ingredient": "oil for frying"}
        ]),
        instructions=json.dumps([
            {"instruction": "In a large bowl, combine soy sauce, vinegar, garlic, bay leaves, and black pepper."},
            {"instruction": "Add chicken pieces and marinate for at least 30 minutes."},
            {"instruction": "In a large pot, heat oil and brown the chicken on all sides."},
            {"instruction": "Add the marinade and water, and simmer for 40 minutes until the chicken is tender."},
            {"instruction": "Serve with rice."}
        ]),
        tags="Filipino, savory, chicken",
        owner_id=4,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
    )

    recipe7 = Recipe(
        id=7,
        name="Gina's Cannoli",
        yield_servings=6,
        prep_time=25,
        cook_time=10,
        total_time=35,
        short_description="Crispy pastry shells filled with creamy ricotta filling.",
        cuisine="Italian",
        description="A classic Italian dessert with a crunchy shell and sweet ricotta filling.",
        ingredients=json.dumps([
            {"ingredient": "Cannoli shells"},
            {"ingredient": "ricotta cheese"},
            {"ingredient": "powdered sugar"},
            {"ingredient": "vanilla extract"},
            {"ingredient": "chocolate chips"},
            {"ingredient": "cinnamon"}
        ]),
        instructions=json.dumps([
            {"instruction": "In a bowl, mix ricotta, powdered sugar, vanilla extract, and cinnamon."},
            {"instruction": "Fill cannoli shells with the ricotta mixture."},
            {"instruction": "Sprinkle with chocolate chips and serve."}
        ]),
        tags="dessert, Italian, sweet",
        owner_id=4,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
    )

    recipe8 = Recipe(
        id=8,
        name="Lisa's Sinigang",
        yield_servings=4,
        prep_time=15,
        cook_time=60,
        total_time=75,
        short_description="A tangy, savory Filipino soup with a tamarind-based broth.",
        cuisine="Filipino",
        description="A hearty Filipino soup made with pork, shrimp, or fish, and a tangy tamarind base.",
        ingredients=json.dumps([
            {"ingredient": "Pork, shrimp, or fish"},
            {"ingredient": "tamarind paste"},
            {"ingredient": "water"},
            {"ingredient": "tomatoes"},
            {"ingredient": "onions"},
            {"ingredient": "long green beans"},
            {"ingredient": "eggplant"},
            {"ingredient": "radish"},
            {"ingredient": "spinach or kangkong"}
        ]),
        instructions=json.dumps([
            {"instruction": "In a large pot, combine water, tamarind paste, tomatoes, and onions."},
            {"instruction": "Bring to a boil and simmer for 30 minutes."},
            {"instruction": "Add pork, shrimp, or fish and cook until tender."},
            {"instruction": "Add vegetables and cook until tender."},
            {"instruction": "Season with salt to taste and serve with rice."}
        ]),
        tags="Filipino, soup, savory, tangy",
        owner_id=4,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
    )

    recipe9 = Recipe(
        id=9,
        name="Dad's Fried Filipino Plantains",
        yield_servings=4,
        prep_time=5,
        cook_time=10,
        total_time=15,
        short_description="Sweet and crispy fried plantains, a popular Filipino snack.",
        cuisine="Filipino",
        description="Golden, crispy plantains fried to perfection and enjoyed as a snack or side dish.",
        ingredients=json.dumps([
            {"ingredient": "Plantains"},
            {"ingredient": "vegetable oil"},
            {"ingredient": "brown sugar"}
        ]),
        instructions=json.dumps([
            {"instruction": "Peel and slice the plantains into rounds."},
            {"instruction": "Heat oil in a frying pan."},
            {"instruction": "Fry the plantains until golden and crispy."},
            {"instruction": "Sprinkle with brown sugar and serve."}
        ]),
        tags="Filipino, snack, sweet, fried",
        owner_id=4,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
    )

    recipe10 = Recipe(
        id=10,
        name="Gina's Taco Soup",
        yield_servings=6,
        prep_time=15,
        cook_time=30,
        total_time=45,
        short_description="A hearty, spicy, and flavorful taco-inspired soup.",
        cuisine="American",
        description="A delicious soup with all the flavors of a taco, perfect for a cozy meal.",
        ingredients=json.dumps([
            {"ingredient": "Ground beef or turkey"},
            {"ingredient": "onion"},
            {"ingredient": "garlic"},
            {"ingredient": "taco seasoning"},
            {"ingredient": "tomatoes"},
            {"ingredient": "black beans"},
            {"ingredient": "corn"},
            {"ingredient": "chicken broth"},
            {"ingredient": "cheese, sour cream, and tortilla chips for topping"}
        ]),
        instructions=json.dumps([
            {"instruction": "In a large pot, brown the ground beef or turkey with onion and garlic."},
            {"instruction": "Add taco seasoning, tomatoes, black beans, corn, and chicken broth."},
            {"instruction": "Simmer for 20 minutes."},
            {"instruction": "Serve with cheese, sour cream, and tortilla chips."}
        ]),
        tags="soup, taco, savory, hearty",
        owner_id=4,
        visibility="Everyone",
        created_at=created_at_time,
        updated_at=created_at_time,
    )

    # Add the recipes to the session
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.add(recipe3)
    db.session.add(recipe4)
    db.session.add(recipe5)
    db.session.add(recipe6)
    db.session.add(recipe7)
    db.session.add(recipe8)
    db.session.add(recipe9)
    db.session.add(recipe10)

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
