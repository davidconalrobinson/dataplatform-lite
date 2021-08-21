"""
Create database.
"""


# Imports.
from src.database.base import *
from src.database.objects import *
from src.config_loader import schema, trigger_functions


def before_create(Base, schema):
	"""
	Steps before creating database:
		- create schema
		- enable uuid extension
	"""
	def before_create(target, connection, **kwargs):
		sql=text("""
			CREATE SCHEMA IF NOT EXISTS {schema};
			CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
			""".format(schema=schema))
		connection.execute(sql)
	event.listen(Base.metadata, 'before_create', before_create)


def after_create(Base, trigger_functions=[]):
	"""
	Create functions after creating database.
	"""
	def after_create(target, connection, **kwargs):
		sql=trigger_functions
		if sql:
			connection.execute(text(''.join(set(sql))))
	event.listen(Base.metadata, 'after_create', after_create)


def create_all(Base, schema, engine):
	"""
	Create schema and database.
	"""
	before_create(Base, schema)
	after_create(Base, trigger_functions)
	Base.metadata.create_all(engine)


if __name__ == '__main__':
	create_all(Base, schema, engine)
