"""Add phone number column in users table

Revision ID: 2a54894030c5
Revises: 
Create Date: 2026-02-16 15:17:47.079010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a54894030c5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
