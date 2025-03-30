from sqlalchemy import Column, Integer, String, DateTime, Float, Time, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key = True)
    country = Column(String(32), nullable = False)
    location_name  = Column(String(22), nullable = False)
    last_updated = Column(DateTime, nullable = False)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_degree = Column(Integer)
    wind_direction = Column(String(3))
    sunrise = Column(Time)
    sunset = Column(Time)

class Precipitations(Base):
    __tablename__ = "precipitations"

    id = Column(Integer, primary_key = True)
    country = Column(String(32), nullable = False)
    location_name  = Column(String(22), nullable = False)
    last_updated = Column(DateTime, nullable = False)
    precipitation = Column(Float)
    humidity = Column(Integer)
    cloud_coverage = Column(Integer)
    good_weather = Column(Boolean)

def get_weather_conditions(country, location, last_updated):
    engine = create_engine("postgresql://postgres:12345678@localhost/bd_lab3")
    with Session(engine) as session:
        precip = session.query(Precipitations).filter_by(country = country, location_name = location, last_updated = last_updated).first()
        weather = session.query(Weather).filter_by(country = country, location_name = location, last_updated = last_updated).first()
        if weather is None:
            return None
        else:
            return (weather.temperature, weather.wind_speed, weather.wind_direction, precip.precipitation, precip.humidity, precip.cloud_coverage, precip.good_weather)
        

def get_weather_for_day(country, location, date):
    engine = create_engine("postgresql://postgres:12345678@localhost/bd_lab3")
    with Session(engine) as session:
        precip = session.query(Precipitations).filter_by(country = country, location_name = location)\
            .filter(Precipitations.last_updated > date + " 00:00", Precipitations.last_updated < date + " 24:00")
        weather = session.query(Weather).filter_by(country = country, location_name = location)\
            .filter(Weather.last_updated > date + " 00:00", Weather.last_updated < date + " 24:00")
        info = []
        for p, w in zip(precip, weather):
            info.append((w.last_updated, w.temperature, w.wind_speed, w.wind_direction, p.precipitation, p.humidity, p.cloud_coverage, p.good_weather))
        if len(info) > 0:
            return info
        else:
            return None