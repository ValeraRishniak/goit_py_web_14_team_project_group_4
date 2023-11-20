"""Init

Revision ID: 652f935c5823
Revises: 
Create Date: 2023-11-20 12:04:07.250684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '652f935c5823'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('role', sa.Enum('admin', 'moderator', 'user', name='role'), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.Column('image_url', sa.String(length=300), nullable=True),
    sa.Column('transform_url', sa.String(length=500), nullable=True),
    sa.Column('public_id', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.String(length=25), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tag_name')
    )
    op.create_table('Qr_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('photo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['images.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment_description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('update_status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image_m2m_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image_m2m_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image_m2m_comment')
    op.drop_table('image_m2m_tag')
    op.drop_table('comments')
    op.drop_table('Qr_codes')
    op.drop_table('tags')
    op.drop_table('images')
    op.drop_table('users')
    # ### end Alembic commands ###
