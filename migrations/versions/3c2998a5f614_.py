"""empty message

Revision ID: 3c2998a5f614
Revises: 4ca4d48829c2
Create Date: 2014-03-19 23:17:49.210912

"""

# revision identifiers, used by Alembic.
revision = '3c2998a5f614'
down_revision = '4ca4d48829c2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('release', sa.Integer(), nullable=True))
    op.add_column('release', sa.Column('package', sa.Integer(), nullable=True))
    op.add_column('release', sa.Column('user', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('release', 'user')
    op.drop_column('release', 'package')
    op.drop_column('file', 'release')
    ### end Alembic commands ###