"""empty message

Revision ID: c037538961da
Revises: 027181457e39
Create Date: 2018-09-01 16:38:33.498316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c037538961da'
down_revision = '027181457e39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'deleted')
    # ### end Alembic commands ###