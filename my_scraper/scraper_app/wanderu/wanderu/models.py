from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

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
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    tripid = Column('tripid', String)
    carrier = Column('carrier', String)
