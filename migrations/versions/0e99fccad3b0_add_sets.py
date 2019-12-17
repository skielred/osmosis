"""add sets

Revision ID: 0e99fccad3b0
Revises: 050735018529
Create Date: 2019-12-16 16:12:36.613365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e99fccad3b0'
down_revision = '050735018529'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('chart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hash', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('max_combo', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('ranked', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('set_id', sa.Integer(), nullable=True))

    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hash', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('score', schema=None) as batch_op:
        batch_op.drop_column('hash')

    with op.batch_alter_table('chart', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('set_id')
        batch_op.drop_column('ranked')
        batch_op.drop_column('max_combo')
        batch_op.drop_column('hash')

    op.drop_table('set')
    # ### end Alembic commands ###