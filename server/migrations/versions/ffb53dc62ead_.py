"""empty message

Revision ID: ffb53dc62ead
Revises: 5835dd4a2d66
Create Date: 2024-02-21 16:09:01.524679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffb53dc62ead'
down_revision = '5835dd4a2d66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('categories')
    op.drop_table('users')
    op.drop_table('recipes')
    op.drop_table('meal_plans')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meal_plans',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('recipe_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], name='fk_meal_plans_recipe_id_recipes'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_meal_plans_user_id_users'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('ingredients', sa.VARCHAR(), nullable=True),
    sa.Column('directions', sa.VARCHAR(), nullable=True),
    sa.Column('category_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name='fk_recipes_category_id_categories'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
