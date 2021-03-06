"""empty message

Revision ID: a2caf7a4c1bb
Revises: 32af209364e0
Create Date: 2020-07-15 12:15:34.263415

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a2caf7a4c1bb'
down_revision = '32af209364e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nickname', sa.String(length=100), nullable=True))
    op.drop_index('Nickname', table_name='users')
    op.create_unique_constraint(None, 'users', ['nickname'])
    op.drop_column('users', 'Nickname')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('Nickname', mysql.VARCHAR(length=100), nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_index('Nickname', 'users', ['Nickname'], unique=True)
    op.drop_column('users', 'nickname')
    # ### end Alembic commands ###
