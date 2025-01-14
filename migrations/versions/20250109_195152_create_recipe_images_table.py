"""create recipe images table

Revision ID: 1edd0f7cac91
Revises: 55ae93091b64
Create Date: 2025-01-09 19:51:52.026725

"""
from alembic import op
import sqlalchemy as sa

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")


# revision identifiers, used by Alembic.
revision = '1edd0f7cac91'
down_revision = '55ae93091b64'
branch_labels = None
depends_on = None


def upgrade():
    schema = os.environ.get("SCHEMA") if environment == "production" else None

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=False),
    sa.Column('caption', sa.String(length=255), nullable=True),
    sa.Column('is_preview', sa.Boolean(), nullable=False),
    sa.Column('uploaded_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema=schema
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_images')
    # ### end Alembic commands ###
