"""Add owner_id to Product model

Revision ID: a8ba664b1ed2
Revises: 09e47cfc8472
Create Date: 2025-08-26 15:31:40.761932

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a8ba664b1ed2"
down_revision = "09e47cfc8472"
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add column as nullable (temporary)
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))

    # Step 2: Backfill old rows with a default user (assume admin with id=1 exists)
    op.execute("UPDATE products SET owner_id = 1 WHERE owner_id IS NULL")

    # Step 3: Now make it NOT NULL and add foreign key constraint
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.alter_column("owner_id", nullable=False)
        batch_op.create_foreign_key(None, "users", ["owner_id"], ["id"])


def downgrade():
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("owner_id")
