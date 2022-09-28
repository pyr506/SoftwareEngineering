"""empty message

Revision ID: a490af0bd60e
Revises: 9855924da325
Create Date: 2021-01-12 09:13:55.526793

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a490af0bd60e'
down_revision = '9855924da325'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('specific_periods', 'project_content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('specific_periods', sa.Column('project_content', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###