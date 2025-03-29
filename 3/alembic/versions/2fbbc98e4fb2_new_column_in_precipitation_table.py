"""new column in precipitation table

Revision ID: 2fbbc98e4fb2
Revises: af49f8119623
Create Date: 2025-03-29 21:42:41.361682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy.orm as orm
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fbbc98e4fb2'
down_revision: Union[str, None] = 'af49f8119623'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class Base(orm.DeclarativeBase):
    pass


class Precipitations(Base):
    __tablename__ = "precipitations"

    id = sa.Column(sa.Integer, primary_key = True)
    country = sa.Column(sa.String(32), nullable = False)
    location_name  = sa.Column(sa.String(22), nullable = False)
    last_updated = sa.Column(sa.DateTime, nullable = False)
    precipitation = sa.Column(sa.Float)
    humidity = sa.Column(sa.Integer)
    cloud_coverage = sa.Column(sa.Integer)
    good_weather = sa.Column(sa.Boolean)


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("precipitations", sa.Column("good_weather", sa.Boolean))
    bind = op.get_bind()
    session = orm.Session(bind = bind)
    precip = session.query(Precipitations)
    for row in precip:
        if (row.cloud_coverage > 75) or (row.precipitation > 1.5) or (row.humidity < 25) or (row.humidity > 90):
            row.good_weather = False
        else:
            row.good_weather = True
    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("precipitations", "good_weather")
