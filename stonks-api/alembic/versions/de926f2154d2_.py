"""empty message

Revision ID: de926f2154d2
Revises: b5163878b215
Create Date: 2021-05-02 17:10:14.530702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de926f2154d2'
down_revision = 'b5163878b215'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('last_price_update', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'last_price_update')
    # ### end Alembic commands ###
