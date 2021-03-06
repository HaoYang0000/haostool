"""add contact_email in comment table

Revision ID: fe75aeca12a8
Revises: df8fc1932b64
Create Date: 2020-06-17 21:20:33.606141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe75aeca12a8'
down_revision = 'df8fc1932b64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('contact_email', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'contact_email')
    # ### end Alembic commands ###
