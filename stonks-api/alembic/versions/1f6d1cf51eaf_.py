"""empty message

Revision ID: 1f6d1cf51eaf
Revises: c22c775d03d8
Create Date: 2021-04-18 22:21:35.060063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f6d1cf51eaf'
down_revision = 'c22c775d03d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stonks', sa.Column('average_price', sa.Numeric(precision=15, scale=4), nullable=False))
    op.add_column('stonks', sa.Column('high_price', sa.Numeric(precision=15, scale=4), nullable=False))
    op.add_column('stonks', sa.Column('low_price', sa.Numeric(precision=15, scale=4), nullable=False))
    op.add_column('stonks', sa.Column('median_price', sa.Numeric(precision=15, scale=4), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stonks', 'median_price')
    op.drop_column('stonks', 'low_price')
    op.drop_column('stonks', 'high_price')
    op.drop_column('stonks', 'average_price')
    # ### end Alembic commands ###