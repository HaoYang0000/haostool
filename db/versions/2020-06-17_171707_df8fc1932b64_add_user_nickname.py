"""add user nickname

Revision ID: df8fc1932b64
Revises: 526ac63e9e54
Create Date: 2020-06-17 17:17:07.611574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df8fc1932b64'
down_revision = '526ac63e9e54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nickname', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'nickname')
    # ### end Alembic commands ###
