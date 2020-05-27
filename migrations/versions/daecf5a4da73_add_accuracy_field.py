"""Add accuracy field

Revision ID: daecf5a4da73
Revises: c3366a1661c4
Create Date: 2020-05-27 03:11:57.417929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daecf5a4da73'
down_revision = 'c3366a1661c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.add_column(sa.Column('accuracy', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.drop_column('accuracy')

    # ### end Alembic commands ###
