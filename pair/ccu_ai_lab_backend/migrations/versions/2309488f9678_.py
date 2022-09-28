"""empty message

Revision ID: 2309488f9678
Revises: a6be14b08c80
Create Date: 2021-01-12 16:53:38.968319

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2309488f9678'
down_revision = 'a6be14b08c80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('specific_periods', sa.Column('country', sa.String(length=64), nullable=True))
    op.drop_column('specific_periods', 'nation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('specific_periods', sa.Column('nation', mysql.VARCHAR(length=64), nullable=True))
    op.drop_column('specific_periods', 'country')
    # ### end Alembic commands ###
