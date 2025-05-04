"""Initial migration

Revision ID: 5e87b4da41a2
Revises: 
Create Date: 2023-09-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e87b4da41a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create posts table
    op.create_table('posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('flagged_reasons', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.CheckConstraint("status IN ('draft', 'flagged', 'approved', 'published')"),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')
