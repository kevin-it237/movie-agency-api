"""empty message

Revision ID: 937f91481c50
Revises: 66fff985c29c
Create Date: 2021-06-14 23:43:27.811726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '937f91481c50'
down_revision = '66fff985c29c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'release_date2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('release_date2', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###