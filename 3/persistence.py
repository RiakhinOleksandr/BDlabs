from sqlalchemy import Column, Integer, String, DateTime, Float, Time
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import DeclarativeBase, Session
import pandas as pd

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
    precipitation = Column(Float)
    humidity = Column(Integer)
    cloud_coverage = Column(Integer)
    sunrise = Column(Time)
    sunset = Column(Time)

try:    
    columns = ["country", "location_name", "last_updated", "temperature_celsius", "wind_kph", "wind_degree", "wind_direction", "precip_mm", "humidity", "cloud", "sunrise", "sunset"]
    df = pd.read_csv("GlobalWeatherRepository.csv", usecols = columns)
    
    engine = create_engine("postgresql://postgres:12345678@localhost/bd_lab3")
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for i in range(df.shape[0]):
            if session.query(Weather).filter_by(country = df.loc[i, "country"], location_name = df.loc[i, "location_name"], last_updated = df.loc[i, "last_updated"]).first() is None:
                weather = Weather(country = df.loc[i, "country"], location_name = df.loc[i, "location_name"], last_updated = df.loc[i, "last_updated"],
                                  temperature = float(df.loc[i, "temperature_celsius"]), wind_speed = float(df.loc[i, "wind_kph"]), 
                                  wind_degree = int(df.loc[i, "wind_degree"]), wind_direction = df.loc[i, "wind_direction"], 
                                  precipitation = float(df.loc[i, "precip_mm"]), humidity = int(df.loc[i, "humidity"]),
                                  cloud_coverage = int(df.loc[i, "cloud"]), sunrise = df.loc[i, "sunrise"], sunset = df.loc[i, "sunset"])
                session.add(weather)
                session.commit()
except Exception as e:
    print(f"Could not connect to database! {repr(e)}")