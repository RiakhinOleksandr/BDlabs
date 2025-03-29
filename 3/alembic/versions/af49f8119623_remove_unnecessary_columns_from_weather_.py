"""remove unnecessary columns from weather table

Revision ID: af49f8119623
Revises: 10d6144f99c0
Create Date: 2025-03-28 14:58:11.362142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af49f8119623'
down_revision: Union[str, None] = '10d6144f99c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("weather", "precipitation")
    op.drop_column("weather", "humidity")
    op.drop_column("weather", "cloud_coverage")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("weather", sa.Column("precipitation", sa.Float))
    op.add_column("weather", sa.Column("humidity", sa.Integer))
    op.add_column("weather", sa.Column("cloud_coverage", sa.Integer))