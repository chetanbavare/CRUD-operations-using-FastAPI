"""add last few columns in posts

Revision ID: fcbb9d4f34be
Revises: 6f463c2f619c
Create Date: 2023-10-19 14:45:03.849072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcbb9d4f34be'
down_revision: Union[str, None] = '6f463c2f619c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published", sa.Boolean(), nullable=False, server_default="True"))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
