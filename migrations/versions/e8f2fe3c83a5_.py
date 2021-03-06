"""empty message

Revision ID: e8f2fe3c83a5
Revises: 5e237346ae3a
Create Date: 2020-07-15 12:27:18.595203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8f2fe3c83a5'
down_revision = '5e237346ae3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nickname', sa.String(length=100), nullable=True))
    op.create_unique_constraint(None, 'users', ['nickname'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'nickname')
    # ### end Alembic commands ###
