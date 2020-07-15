"""add star to videoModel

Revision ID: 5e6fdbb36f9f
Revises: fa4d166832e8
Create Date: 2020-07-14 23:13:41.006279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e6fdbb36f9f'
down_revision = 'fa4d166832e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('star', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'star')
    # ### end Alembic commands ###
