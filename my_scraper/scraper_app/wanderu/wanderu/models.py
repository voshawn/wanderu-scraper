from sqlalchemy import create_engine, Column, String, Integer, DateTime, Float, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import datetime
import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_trips_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Trips(DeclarativeBase):
    """Sqlalchemy trips model"""
    __tablename__ = "trips_load"

    id = Column(Integer, primary_key=True)
    tripid = Column('tripid', String)
    carrier = Column('carrier', String)
    originTime = Column('origintime', Time)
    originCity = Column('origincity', String)
    originLocation = Column('originlocation', String)
    destinationTime = Column('destinationtime', Time)
    destinationCity = Column('destinationcity', String)
    destinationLocation = Column('destinationlocation', String)
    price = Column('price', Float)
    duration = Column('duration', String)
    features = Column('features', String)
    dateoftrip = Column('dateoftrip', DateTime)
    datescraped = Column(DateTime, default=datetime.datetime.utcnow)
    soldout = Column('soldout', String)
