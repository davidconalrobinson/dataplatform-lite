"""
Create database.
"""


# Imports.
from src.database.base import *
from src.database.objects import *
from src.config_loader import schema


if __name__ == '__main__':
	create_schema(Base, schema)
	Base.metadata.create_all(engine)
