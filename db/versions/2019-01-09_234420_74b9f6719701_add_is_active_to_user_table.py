"""Add is_active to user table

Revision ID: 74b9f6719701
Revises: 9c39e466aaeb
Create Date: 2019-01-09 23:44:20.119278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74b9f6719701'
down_revision = '9c39e466aaeb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_accounting_tag_user_id', 'account_tags', type_='foreignkey')
    op.create_foreign_key('fk_accounting_tag_user_id', 'account_tags', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_active')
    op.drop_constraint('fk_accounting_tag_user_id', 'account_tags', type_='foreignkey')
    op.create_foreign_key('fk_accounting_tag_user_id', 'account_tags', 'users', ['id'], ['id'])
    # ### end Alembic commands ###
