"""empty message

Revision ID: 0c026cf182e7
Revises: 4d50dca74025
Create Date: 2021-05-04 14:59:37.321983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c026cf182e7'
down_revision = '4d50dca74025'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stonks', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stonks', 'created_at')
    # ### end Alembic commands ###
