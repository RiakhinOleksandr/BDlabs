"""create precipitation table

Revision ID: 10d6144f99c0
Revises: 
Create Date: 2025-03-28 13:43:27.373838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy.orm as orm
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10d6144f99c0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class Base(orm.DeclarativeBase):
    pass


class Weather(Base):
    __tablename__ = "weather"

    id = sa.Column(sa.Integer, primary_key = True)
    country = sa.Column(sa.String(32), nullable = False)
    location_name  = sa.Column(sa.String(22), nullable = False)
    last_updated = sa.Column(sa.DateTime, nullable = False)
    temperature = sa.Column(sa.Float)
    wind_speed = sa.Column(sa.Float)
    wind_degree = sa.Column(sa.Integer)
    wind_direction = sa.Column(sa.String(3))
    precipitation = sa.Column(sa.Float)
    humidity = sa.Column(sa.Integer)
    cloud_coverage = sa.Column(sa.Integer)
    sunrise = sa.Column(sa.Time)
    sunset = sa.Column(sa.Time)


class Precipitations(Base):
    __tablename__ = "precipitations"

    id = sa.Column(sa.Integer, primary_key = True)
    country = sa.Column(sa.String(32), nullable = False)
    location_name  = sa.Column(sa.String(22), nullable = False)
    last_updated = sa.Column(sa.DateTime, nullable = False)
    precipitation = sa.Column(sa.Float)
    humidity = sa.Column(sa.Integer)
    cloud_coverage = sa.Column(sa.Integer)


def upgrade() -> None:
    """Upgrade schema."""
    table = op.create_table(
        "precipitations",
        sa.Column("id", sa.Integer, primary_key = True),
        sa.Column("country", sa.String(32), nullable = False),
        sa.Column("location_name", sa.String(22), nullable = False),
        sa.Column("last_updated", sa.DateTime, nullable = False),
        sa.Column("precipitation", sa.Float),
        sa.Column("humidity", sa.Integer),
        sa.Column("cloud_coverage", sa.Integer)
    )
    bind = op.get_bind()
    session = orm.Session(bind = bind)
    data = session.query(Weather)
    dcts = []
    for row in data:
        dct = {"id" : row.id, "country" : row.country, "location_name" : row.location_name,
               "last_updated" : row.last_updated, "precipitation" : row.precipitation,
               "humidity" : row.humidity, "cloud_coverage" : row.cloud_coverage}
        dcts.append(dct)
    op.bulk_insert(table, dcts)


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    session = orm.Session(bind = bind)
    precip = session.query(Precipitations)
    weather = session.query(Weather)
    for p, w in zip(precip, weather):
        w.precipitation = p.precipitation
        w.humidity = p.humidity
        w.cloud_coverage = p.cloud_coverage
    session.commit()
    op.drop_table("precipitations")
