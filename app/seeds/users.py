from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo users
def seed_users():
    # Adds demo users, recipes, and related models
    demo = User(
        username='demo', email='demo@aa.io', password='password', first_name='Demo',
        bio='This is a demo user.', profile_image_url='http://example.com/demo-profile.jpg', location='Demo City')
    marnie = User(
        username='marnie', email='marnie@aa.io', password='password', first_name='Marnie',
        bio='This is Marnie’s profile.', profile_image_url='http://example.com/marnie-profile.jpg', location='Marnie City')
    bobbie = User(
        username='bobbie', email='bobbie@aa.io', password='password', first_name='Bobbie',
        bio='Bobbie’s bio goes here.', profile_image_url='http://example.com/bobbie-profile.jpg', location='Bobbie City')
    lainey = User(
        username='lainey', email='lainey@email.com', password='mango', first_name='Lainey',
        bio='Lainey&;apos bio goes here.', profile_image_url='http://example.com/bobbie-profile.jpg', location='San Francisco')


    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
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
