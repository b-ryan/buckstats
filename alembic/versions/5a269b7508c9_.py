"""empty message

Revision ID: 5a269b7508c9
Revises: 3508973368c4
Create Date: 2014-02-03 10:59:40.952190

"""

# revision identifiers, used by Alembic.
revision = '5a269b7508c9'
down_revision = '3508973368c4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_key', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_keys')
    ### end Alembic commands ###