"""增加标签表

Revision ID: b027ad948f79
Revises: 6b9fb491c9a6
Create Date: 2019-05-21 10:58:20.285837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b027ad948f79'
down_revision = '6b9fb491c9a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('rank', sa.Float(), nullable=True))
    op.create_index(op.f('ix_posts_rank'), 'posts', ['rank'], unique=False)
    op.add_column('tags', sa.Column('rank', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'rank')
    op.drop_index(op.f('ix_posts_rank'), table_name='posts')
    op.drop_column('posts', 'rank')
    # ### end Alembic commands ###
