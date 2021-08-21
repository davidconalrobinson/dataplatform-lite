"""
Create database.
"""


# Imports.
from src.database.base import *
from src.database.objects import *
from src.config_loader import schema


def create_schema(Base, schema):
	"""
	Create schema before creating database.
	"""
	def before_create(target, connection, **kwargs):
		sql=text('CREATE SCHEMA IF NOT EXISTS {schema};'.format(schema=schema))
		connection.execute(sql)
	event.listen(Base.metadata, 'before_create', before_create)


def create_all(Base, schema, engine):
	"""
	Create schema and database.
	"""
	create_schema(Base, schema)
	Base.metadata.create_all(engine)


if __name__ == '__main__':
	create_all(Base, schema, engine)
