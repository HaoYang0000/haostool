"""add unknown_user_name to comment

Revision ID: 6dea29371128
Revises: e0db8f218320
Create Date: 2020-06-16 19:58:29.887297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dea29371128'
down_revision = 'e0db8f218320'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('unknown_user_name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'unknown_user_name')
    # ### end Alembic commands ###
