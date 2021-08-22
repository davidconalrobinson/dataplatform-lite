"""
Create SQL Alchemy engine, session and base class.
"""


# Imports.
from sqlalchemy import create_engine, event
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.config_loader import username, password, host, port, database


# Create session.
engine=create_engine('postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, database))
Session=sessionmaker(bind=engine)


# Create base class.
Base=declarative_base()
