"""empty message

Revision ID: 853e6c8522c1
Revises: b002c603fdb7
Create Date: 2021-04-18 22:24:23.531289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '853e6c8522c1'
down_revision = 'b002c603fdb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer', sa.Column('category', sa.String(length=32), nullable=False))
    op.add_column('offer', sa.Column('currency', sa.String(length=3), nullable=False))
    op.add_column('offer', sa.Column('price', sa.Numeric(precision=15, scale=4), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offer', 'price')
    op.drop_column('offer', 'currency')
    op.drop_column('offer', 'category')
    # ### end Alembic commands ###