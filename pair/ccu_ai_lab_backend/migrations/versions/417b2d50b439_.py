"""empty message

Revision ID: 417b2d50b439
Revises: 8a41d475a3c5
Create Date: 2021-01-25 18:17:44.920165

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '417b2d50b439'
down_revision = '8a41d475a3c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('title', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64), nullable=True))
    # ### end Alembic commands ###
