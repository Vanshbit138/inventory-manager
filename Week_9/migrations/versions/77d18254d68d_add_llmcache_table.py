"""Add LLMCache table

Revision ID: 77d18254d68d
Revises: 6568d4b91f72
Create Date: 2025-09-08 15:13:01.042182

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "77d18254d68d"
down_revision = "6568d4b91f72"
branch_labels = None
depends_on = None


def upgrade():
    # Only create llm_cache table
    op.create_table(
        "llm_cache",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("question"),
    )


def downgrade():
    # Only drop llm_cache table
    op.drop_table("llm_cache")
