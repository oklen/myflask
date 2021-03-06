"""empty message

Revision ID: e028c3129b72
Revises: 
Create Date: 2017-10-29 14:03:53.755194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e028c3129b72'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=80), nullable=False),
    sa.Column('duration', sa.Numeric(), nullable=False),
    sa.Column('created_time', sa.DATETIME(), nullable=True),
    sa.Column('printed_times', sa.Integer(), nullable=False),
    sa.Column('printed_once', sa.Boolean(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_message'), 'message', ['message'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_message_message'), table_name='message')
    op.drop_table('message')
    op.drop_table('category')
    # ### end Alembic commands ###
