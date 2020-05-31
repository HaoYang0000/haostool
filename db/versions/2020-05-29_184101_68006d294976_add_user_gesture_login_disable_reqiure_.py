"""add user gesture login, disable reqiure for first name last name

Revision ID: 68006d294976
Revises: 5974ce877b2c
Create Date: 2020-05-29 18:41:01.902296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '68006d294976'
down_revision = '5974ce877b2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('gesture_hash', sa.String(length=255), nullable=True))
    op.alter_column('users', 'first_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'last_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.drop_column('users', 'gesture_hash')
    # ### end Alembic commands ###