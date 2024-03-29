"""Add image field

Revision ID: 8576adc2af63
Revises: 
Create Date: 2023-08-18 17:44:07.179782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8576adc2af63'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
