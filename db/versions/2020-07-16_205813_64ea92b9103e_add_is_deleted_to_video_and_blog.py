"""Add is deleted to video and blog

Revision ID: 64ea92b9103e
Revises: ff8921fc845c
Create Date: 2020-07-16 20:58:13.690533

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '64ea92b9103e'
down_revision = 'ff8921fc845c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'is_published')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('is_published', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
