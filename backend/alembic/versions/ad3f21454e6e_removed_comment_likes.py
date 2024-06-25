"""Removed comment likes

Revision ID: ad3f21454e6e
Revises: 6c6d256a5a51
Create Date: 2024-06-25 10:31:46.479103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad3f21454e6e'
down_revision: Union[str, None] = '6c6d256a5a51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('CommentLikes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CommentLikes',
    sa.Column('comment_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['Comment.id'], name='comment_likes_comment_id'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], name='comment_likes_user_id')
    )
    # ### end Alembic commands ###
