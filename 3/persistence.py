from sqlalchemy import Column, Integer, String, DateTime, Float, Time, Boolean
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
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

try:    
    engine_postgr = create_engine("postgresql://postgres:12345678@localhost/bd_lab3")
    with Session(engine_postgr) as session_postgr:
        weather = session_postgr.query(Weather)
        precip = session_postgr.query(Precipitations)
    engine_mysql = create_engine("mysql+pymysql://root:123456789@localhost/bd_lab3")
    if not database_exists(engine_mysql.url):
        create_database(engine_mysql.url)
    Base.metadata.create_all(engine_mysql)
    with Session(engine_mysql) as session:
        for w in weather:
            if session.query(Weather).filter_by(id = w.id).first() is None:
                weath = Weather(id = w.id, country = w.country, location_name = w.location_name, last_updated = w.last_updated,
                            temperature = w.temperature, wind_speed = w.wind_speed, wind_degree = w.wind_degree,
                            wind_direction = w.wind_direction, sunrise = w.sunrise, sunset = w.sunset)
                session.add(weath)
                session.commit()
        for p in precip:
            if session.query(Precipitations).filter_by(id = p.id).first() is None:
                pr = Precipitations(id = p.id, country = p.country, location_name = p.location_name, 
                                last_updated = p.last_updated, precipitation = p.precipitation, humidity = p.humidity, 
                                cloud_coverage = p.cloud_coverage, good_weather = p.good_weather)
                session.add(pr)
                session.commit()
except Exception as e:
    print(f"Could not connect to database! {repr(e)}")