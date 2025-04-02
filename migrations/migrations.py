"""add created_at column to todo table

Revision ID: def67890
Revises: abc12345
Create Date: 2025-04-01 14:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'def67890'
down_revision = 'abc12345'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('todo', sa.Column('created_at', sa.DateTime(), nullable=True))
    # Optionally, you might want to update existing rows to have a default timestamp:
    op.execute("UPDATE todo SET created_at = CURRENT_TIMESTAMP")

def downgrade():
    op.drop_column('todo', 'created_at')