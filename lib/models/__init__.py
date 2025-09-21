import sqlite3

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
ENGINE = create_engine('sqlite:///event_planner.db')
SESSION = sessionmaker(bind=ENGINE)
Base = declarative_base()

# Import models to register them with SQLAlchemy
from .event import Event
from .attendee import Attendee  
from .activity import Activity