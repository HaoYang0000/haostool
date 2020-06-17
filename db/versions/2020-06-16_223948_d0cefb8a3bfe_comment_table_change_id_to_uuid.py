"""comment table change id to uuid

Revision ID: d0cefb8a3bfe
Revises: 6dea29371128
Create Date: 2020-06-16 22:39:48.431233

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd0cefb8a3bfe'
down_revision = '6dea29371128'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('blog_uuid', sa.String(length=225), nullable=True))
    op.add_column('comments', sa.Column('video_uuid', sa.String(length=225), nullable=True))
    op.drop_column('comments', 'video_id')
    op.drop_column('comments', 'blog_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('blog_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('comments', sa.Column('video_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('comments', 'video_uuid')
    op.drop_column('comments', 'blog_uuid')
    # ### end Alembic commands ###