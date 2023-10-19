"""create users table

Revision ID: 85d09b60bd6a
Revises: a1d63bbce57f
Create Date: 2023-10-19 14:43:07.680264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85d09b60bd6a'
down_revision: Union[str, None] = 'a1d63bbce57f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",sa.Column("id", sa.Integer(), nullable=False)
                           ,sa.Column("email", sa.String(), nullable=False)
                           ,sa.Column("password", sa.String(), nullable=False)
                           ,sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()"))
                           ,sa.PrimaryKeyConstraint("id")
                           ,sa.UniqueConstraint("email"))
    
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass