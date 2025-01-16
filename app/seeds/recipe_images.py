from app.models import db, RecipeImage, environment, SCHEMA
from sqlalchemy.sql import text


# Seed data for recipe images with captions
def seed_recipe_images():

    recipe_image1 = RecipeImage(
        image_url="https://data.thefeedfeed.com/static/2021/09/21/1632264639614a61bf03b09.jpg",
        is_preview=True,
        recipe_id=1,
        user_id=1, # Remy
        caption="Plated how we served it to Anton Ego."
    )


    recipe_image2 = RecipeImage(
        image_url="https://www.seriouseats.com/thmb/K8bvy-AQYLQ3PzqZuQlfbuS6A0c=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__serious_eats__seriouseats.com__images__20110106-shack-comparison20-200620copy-4c20bdc6d2a446fcab30a400d1a5323f.jpg",
        is_preview=True,
        recipe_id=5,
        user_id=3, # Colette
        caption="Juicy smash burger with all the fixings."
    )

    recipe_image3 = RecipeImage(
        image_url="https://thealmondeater.com/wp-content/uploads/2023/04/healthy-fettuccine-alfredo_web-6.jpg",
        is_preview=True,
        recipe_id=3,  # Associated with "Chicken Alfredo"
        user_id=3, # Colette
        caption="Creamy chicken alfredo pasta made to perfection."
    )

    recipe_image4 = RecipeImage(
        image_url="https://bellyfull.net/wp-content/uploads/2021/02/Chicken-Alfredo-blog-4.jpg",
        is_preview=False,
        recipe_id=3,
        user_id=3, # Colette
        caption="A close-up of the creamy and comforting chicken alfredo."
    )

    recipe_image5 = RecipeImage(
        image_url="https://www.onceuponachef.com/images/2017/02/Asian-Vegetable-Stir-Fry-3-1700x1223.jpg",
        is_preview=True,
        recipe_id=2,  # Associated with "Veggie Stir-Fry"
        user_id=2, # Alfredo
        caption="Healthy and colorful veggie stir-fry."
    )

    recipe_image6 = RecipeImage(
        image_url="https://thewoksoflife.com/wp-content/uploads/2022/02/vegetable-stir-fry-3.jpg",
        is_preview=False,
        recipe_id=2,
        user_id=2, # Alfredo
        caption="Fresh ingredients for the veggie stir-fry."
    )

    recipe_image7 = RecipeImage(
        image_url="https://www.seriouseats.com/thmb/aEYbrnuKQ3Ge7T5sd3A0BWQGPLY=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20210607-CLASSICSMASHEDBURGS-JANJIGIAN-seriouseats-10-8af40a4a1698459c99e7f3c0df7f6a0f.jpg",
        is_preview=True,
        recipe_id=5,  # Associated with "Papa's Smash Burger"
        user_id=1, #
        caption="Perfectly grilled smash burger with crispy edges."
    )

    recipe_image8 = RecipeImage(
        image_url="https://www.onceuponachef.com/images/2017/02/stir-fry3-1.jpg",
        is_preview=False,
        recipe_id=2,  # Associated with "Veggie Stir-Fry"
        user_id=2, # Alfredo
        caption="Healthy and colorful veggie stir-fry."
    )

    recipe_image9 = RecipeImage(
        image_url="https://www.onceuponachef.com/images/2017/02/stir-fry4-1.jpg",
        is_preview=False,
        recipe_id=2,  # Associated with "Veggie Stir-Fry"
        user_id=2, # Alfredo
        caption="Healthy and colorful veggie stir-fry."
    )

    recipe_image10 = RecipeImage(
        image_url="https://panlasangpinoy.com/wp-content/uploads/2024/04/Filipino-Chicken-Adobo-Recipe.jpg",
        is_preview=True,
        recipe_id=6,  # Associated with "Chicken Adobo Filipino"
        user_id=4,  # User 4
        caption="Classic Filipino chicken adobo, simmered to perfection."
    )

    recipe_image11 = RecipeImage(
        image_url="https://assets.bonappetit.com/photos/5bedd7a0c09fe84a28774cb4/16:9/w_1280,c_limit/cannoli-1.jpg",
        is_preview=True,
        recipe_id=7,  # Associated with "Cannoli"
        user_id=4,  # User 4
        caption="Crispy cannoli filled with sweet ricotta and topped with chocolate."
    )

    recipe_image12 = RecipeImage(
        image_url="https://panlasangpinoy.com/wp-content/uploads/2022/08/pork-and-chicken-sinigang.jpg",
        is_preview=True,
        recipe_id=8,  # Associated with "Sinigang"
        user_id=4,  # User 4
        caption="A bowl of savory, tangy pork sinigang."
    )

    recipe_image13 = RecipeImage(
        image_url="https://panlasangpinoy.com/wp-content/uploads/2011/10/Minatamis-na-Saging.jpg",
        is_preview=True,
        recipe_id=9,  # Associated with "Fried Filipino Plantains"
        user_id=4,  # User 4
        caption="Golden and crispy fried plantains, a sweet Filipino treat."
    )

    recipe_image14 = RecipeImage(
        image_url="https://www.simplyrecipes.com/thmb/Y4DfBsIM1s6fhprPbhLSKpKDn_A=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Stovetop-Taco-Soup-LEAD-06-1f65b29b91734a439d46671c3de894c5.jpg",
        is_preview=True,
        recipe_id=10,  # Associated with "Taco Soup"
        user_id=4,  # User 4
        caption="A hearty, flavorful taco soup, perfect for any meal."
    )

    recipe_image15 = RecipeImage(
        image_url="https://panlasangpinoy.com/wp-content/uploads/2024/04/Chicken-Adobo-Cooking-Steps.jpg",
        is_preview=False,
        recipe_id=6,  # Associated with "Chicken Adobo Filipino"
        user_id=4,  # User 4
        caption="Classic Filipino chicken adobo, simmered to perfection."
    )

    recipe_image16 = RecipeImage(
        image_url="https://panlasangpinoy.com/wp-content/uploads/2024/04/Pinoy-adobo.jpg",
        is_preview=False,
        recipe_id=6,  # Associated with "Chicken Adobo Filipino"
        user_id=4,  # User 4
        caption="Classic Filipino chicken adobo, simmered to perfection."
    )

    recipe_image17 = RecipeImage(
        image_url="https://www.allrecipes.com/thmb/bkXoArv3mjCmhOHKPBkaQUR48dg=/0x512/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/222006-disneys-ratatouille-DDMFS-4x3-36eb15843ab548a79e7aab761dac92e1.jpg",
        is_preview=False,
        recipe_id=1,
        user_id=1, # Remy
        caption=""
    )



    # Add the recipe images to the session
    db.session.add(recipe_image1)
    db.session.add(recipe_image2)
    db.session.add(recipe_image3)
    db.session.add(recipe_image4)
    db.session.add(recipe_image5)
    db.session.add(recipe_image6)
    db.session.add(recipe_image7)
    db.session.add(recipe_image8)
    db.session.add(recipe_image9)
    db.session.add(recipe_image10)
    db.session.add(recipe_image11)
    db.session.add(recipe_image12)
    db.session.add(recipe_image13)
    db.session.add(recipe_image14)
    db.session.add(recipe_image15)
    db.session.add(recipe_image16)
    db.session.add(recipe_image17)
    db.session.commit()

def undo_recipe_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.recipe_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM recipe_images"))
    db.session.commit()
