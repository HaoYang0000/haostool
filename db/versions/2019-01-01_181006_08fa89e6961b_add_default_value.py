"""Add default value

Revision ID: 08fa89e6961b
Revises: 2a235399a9af
Create Date: 2019-01-01 18:10:06.865000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import table, column, Integer, String


# revision identifiers, used by Alembic.
revision = '08fa89e6961b'
down_revision = '2a235399a9af'
branch_labels = None
depends_on = None


def upgrade():
    tags = table('account_tags',
                     column('id', Integer),
                     column('name', String))
    op.bulk_insert(tags,
                   [
                       {'id': 1, 'name': 'Olive Supermarket'}
                   ])


def downgrade():
    tags = table('account_tags',
                     column('id', Integer),
                     column('name', String))
    statusus.delete(tags.c.id == 1)
