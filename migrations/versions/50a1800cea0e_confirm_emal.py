"""confirm emal

Revision ID: 50a1800cea0e
Revises: 67e9f50e89ad
Create Date: 2023-10-30 16:46:23.537467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50a1800cea0e'
down_revision: Union[str, None] = '67e9f50e89ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
