"""Remove is_deleted in video model

Revision ID: f283c0546274
Revises: 64ea92b9103e
Create Date: 2020-08-01 18:55:20.139745

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f283c0546274'
down_revision = '64ea92b9103e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('blog_posts', 'is_deleted')
    # op.drop_column('videos', 'is_deleted')
    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('videos', sa.Column('is_deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    # op.add_column('blog_posts', sa.Column('is_deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
    pass
