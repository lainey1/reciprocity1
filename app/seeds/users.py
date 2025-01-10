from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo users
def seed_users():
    # Adds demo users, recipes, and related models
    demo = User(
        username="the_ratatouille", email="remy@gasteaus.com", password="password", first_name="Demo",
        bio="I discovered my love for cooking by reading Anyone Can Cook by my idol, Auguste Gusteau.",
        profile_image_url="https://static.wikia.nocookie.net/pixar/images/5/56/Ratatouille-remy2.jpg/revision/latest/top-crop/width/200/height/150?cb=20110512131040", location="Paris, France"
    )
    alfredo = User(
        username="i_am_linguini", email="alfredo@gasteaus.com", password="password", first_name="Alfredo",
        bio="I enjoy cooking recipes handed down to me by good friend Remy",
        profile_image_url="https://funkymbti.com/wp-content/uploads/2021/12/alfredo.jpg", location="Paris, France"
    )
    colette = User(
        username="anyone_can_cook", email="colette@aa.io", password="password", first_name="Collette",
        bio="I know every recipe of Anyone Can Cook by heart.", profile_image_url="https://funkymbti.com/wp-content/uploads/2021/12/collette.jpg", location="Paris, France"
    )
    lainey = User(
        username="lainey", email="lainey@email.com", password="mango", first_name="Lainey",
        bio="My go to family recipe is my grandma’s chicken adobo.",
        profile_image_url="http://example.com/bobbie-profile.jpg", location="San Francisco, United States"
    )



    db.session.add(demo)
    db.session.add(alfredo)
    db.session.add(colette)
    db.session.add(lainey)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
