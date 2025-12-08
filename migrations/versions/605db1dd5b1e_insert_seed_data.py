"""Insert seed data

Revision ID: 605db1dd5b1e
Revises: 291e935a1a65
Create Date: 2025-12-08 23:09:03.725329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '605db1dd5b1e'
down_revision = '291e935a1a65'
branch_labels = None
depends_on = None


def upgrade():

    categories_table = sa.table('categories',
                                sa.column('id', sa.Integer),
                                sa.column('name', sa.String)
                                )

    products_table = sa.table('products',
                              sa.column('name', sa.String),
                              sa.column('price', sa.Float),
                              sa.column('active', sa.Boolean),
                              sa.column('category_id', sa.Integer)
                              )


    op.bulk_insert(categories_table, [
        {'id': 10, 'name': 'Skincare 🧴'},
        {'id': 11, 'name': 'Shoes 👠'},
        {'id': 12, 'name': 'Sale 🔥'}
    ])


    op.bulk_insert(products_table, [
        {'name': 'Korean Face Mask', 'price': 5.0, 'active': True, 'category_id': 10},
        {'name': 'Pink Sneakers', 'price': 85.0, 'active': True, 'category_id': 11},
        {'name': 'High Heels', 'price': 150.0, 'active': True, 'category_id': 11},
        {'name': 'Old Collection Dress', 'price': 20.0, 'active': False, 'category_id': 12}
    ])


def downgrade():
    op.execute(
        "DELETE FROM products WHERE name IN ('Korean Face Mask', 'Pink Sneakers', 'High Heels', 'Old Collection Dress')")
    op.execute("DELETE FROM categories WHERE id IN (10, 11, 12)")