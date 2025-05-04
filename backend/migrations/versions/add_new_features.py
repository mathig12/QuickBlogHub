"""Add new features to posts table

Revision ID: e5fc9baf8e12
Revises: 5e87b4da41a2
Create Date: 2025-05-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5fc9baf8e12'
down_revision = '5e87b4da41a2'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to posts table
    op.add_column('posts', sa.Column('tags', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('quality_score', sa.Float(), nullable=True))
    op.add_column('posts', sa.Column('moderation_data', sa.JSON(), nullable=True))
    op.add_column('posts', sa.Column('warnings', sa.Text(), nullable=True))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('posts', sa.Column('published_at', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # Drop added columns
    op.drop_column('posts', 'published_at')
    op.drop_column('posts', 'updated_at')
    op.drop_column('posts', 'warnings')
    op.drop_column('posts', 'moderation_data')
    op.drop_column('posts', 'quality_score')
    op.drop_column('posts', 'tags')