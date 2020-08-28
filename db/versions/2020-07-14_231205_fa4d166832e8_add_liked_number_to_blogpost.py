"""add liked_number to blogpost

Revision ID: fa4d166832e8
Revises: ae9f2b71608c
Create Date: 2020-07-14 23:12:05.071955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa4d166832e8'
down_revision = 'ae9f2b71608c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog_posts', sa.Column('liked_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blog_posts', 'liked_number')
    # ### end Alembic commands ###