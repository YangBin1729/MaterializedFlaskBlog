"""empty message

Revision ID: 5a8522e79e24
Revises: 04bfaed55a91
Create Date: 2019-05-20 10:54:42.304061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a8522e79e24'
down_revision = '04bfaed55a91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collect',
    sa.Column('collector_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['collector_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], )
    )
    op.create_table('like',
    sa.Column('liker_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['liker_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('like')
    op.drop_table('collect')
    # ### end Alembic commands ###
