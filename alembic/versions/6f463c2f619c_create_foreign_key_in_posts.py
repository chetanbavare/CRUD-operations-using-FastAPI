"""create foreign key in posts

Revision ID: 6f463c2f619c
Revises: 85d09b60bd6a
Create Date: 2023-10-19 14:44:19.520880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f463c2f619c'
down_revision: Union[str, None] = '85d09b60bd6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(), nullable=False))
    op.create_foreign_key("posts_foreign_key", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_column("posts","owner_id")
    pass