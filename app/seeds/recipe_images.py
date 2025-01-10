from app.models import db, RecipeImage, environment, SCHEMA
from sqlalchemy.sql import text


# Seed data for recipe images with captions
def seed_recipe_images():
    recipe_image1 = RecipeImage(
        id=1,
        image_url="https://www.seriouseats.com/thmb/aEYbrnuKQ3Ge7T5sd3A0BWQGPLY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20210607-CLASSICSMASHEDBURGS-JANJIGIAN-seriouseats-10-8af40a4a1698459c99e7f3c0df7f6a0f.jpg",
        is_preview=True,
        recipe_id=1,  # Associated with "Dad' Smash Burger"
        user_id=1, # Demo
        caption="Perfectly grilled smash burger with crispy edges."
    )

    recipe_image2 = RecipeImage(
        id=2,
        image_url="https://www.seriouseats.com/thmb/K8bvy-AQYLQ3PzqZuQlfbuS6A0c=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__serious_eats__seriouseats.com__images__20110106-shack-comparison20-200620copy-4c20bdc6d2a446fcab30a400d1a5323f.jpg",
        is_preview=False,
        recipe_id=1,
        user_id=1, # Demo
        caption="Juicy smash burger with all the fixings."
    )

    recipe_image3 = RecipeImage(
        id=3,
        image_url="https://www.foodnetwork.com/content/dam/images/food/fullset/2022/6/10/0/FNK_Chicken_Alfredo_H.jpg",
        is_preview=True,
        recipe_id=3,  # Associated with "Chicken Alfredo"
        user_id=3, # Bobbie
        caption="Creamy chicken alfredo pasta made to perfection."
    )

    recipe_image4 = RecipeImage(
        id=4,
        image_url="https://www.foodnetwork.com/content/dam/images/food/fullset/2022/6/10/0/FNK_Chicken_Alfredo_FoodNetwork_H.jpg",
        is_preview=False,
        recipe_id=3,
        user_id=3, # Bobbie
        caption="A close-up of the creamy and comforting chicken alfredo."
    )

    recipe_image5 = RecipeImage(
        id=5,
        image_url="https://example.com/images/veggie-stirfry-main.jpg",
        is_preview=True,
        recipe_id=2,  # Associated with "Veggie Stir-Fry"
        user_id=2, # Marnie
        caption="Healthy and colorful veggie stir-fry."
    )

    recipe_image6 = RecipeImage(
        id=6,
        image_url="https://example.com/images/veggie-stirfry-ingredients.jpg",
        is_preview=False,
        recipe_id=2,
        user_id=2, # Marnie
        caption="Fresh ingredients for the veggie stir-fry."
    )

    # Add the recipe images to the session
    db.session.add(recipe_image1)
    db.session.add(recipe_image2)
    db.session.add(recipe_image3)
    db.session.add(recipe_image4)
    db.session.add(recipe_image5)
    db.session.add(recipe_image6)
    db.session.commit()

def undo_recipe_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.recipe_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM recipe_images"))
    db.session.commit()
