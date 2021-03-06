"""Add first name last name to user

Revision ID: 9b952096cc92
Revises: 68e7b2846d58
Create Date: 2019-01-10 22:36:28.231444

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9b952096cc92'
down_revision = '68e7b2846d58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('users', sa.Column('first_name', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')

    # ### end Alembic commands ###
