"""add content column to posts

Revision ID: a1d63bbce57f
Revises: bd0f1239d028
Create Date: 2023-10-19 14:42:40.650687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1d63bbce57f'
down_revision: Union[str, None] = 'bd0f1239d028'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
