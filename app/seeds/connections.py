from app.models import db, Connection, environment, SCHEMA
from sqlalchemy.sql import text

# Seed data for connections
def seed_connections():
    connection1 = Connection(
        user_id=1,
        connected_user_id=2,
        connection_type="friend",  # Lainey is friends with Marnie
        status="accepted"
    )

    connection2 = Connection(
        user_id=2,
        connected_user_id=3,
        connection_type="follower",  # Marnie follows Bobbie
        status="pending"
    )

    connection3 = Connection(
        user_id=3,
        connected_user_id=1,
        connection_type="friend",  # Bobbie is friends with Lainey
        status="rejected"
    )

    connection4 = Connection(
        user_id=4,
        connected_user_id=2,
        connection_type="follower",  # Lainey follows Marnie
        status="pending"
    )

    connection5 = Connection(
        user_id=1,
        connected_user_id=3,
        connection_type="family",  # Lainey is family with Bobbie
        status="accepted"
    )

    connection6 = Connection(
        user_id=4,
        connected_user_id=1,
        connection_type="family",  # Bobbie is family with Lainey
        status="accepted"
    )

    db.session.add(connection1)
    db.session.add(connection2)
    db.session.add(connection3)
    db.session.add(connection4)
    db.session.add(connection5)
    db.session.add(connection6)
    db.session.commit()

# Undo seed data
def undo_connections():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.connections RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM connections"))
    db.session.commit()
