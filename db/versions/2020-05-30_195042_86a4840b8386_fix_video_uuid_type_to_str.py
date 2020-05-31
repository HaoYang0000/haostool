"""fix video uuid type to str

Revision ID: 86a4840b8386
Revises: 563c6ec512d2
Create Date: 2020-05-30 19:50:42.654995

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '86a4840b8386'
down_revision = '563c6ec512d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('videos', 'uuid',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.String(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('videos', 'uuid',
               existing_type=sa.String(length=255),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    # ### end Alembic commands ###