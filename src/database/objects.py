"""
Creates a python class for each of the objects defined in config file.

Each class maps to a database table using SQL alchemy ORM.
"""


# Imports.
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import ARRAY
from src.database.base import Base
from src.config.config_loader import schema, objects


# Loop through objects and generate a class for each.
for k0, v0 in objects.items():
	object_dict={
		'__table_args__': {
			'schema' : schema,
			'comment': v0['description']},
		'__tablename__': k0
	}
	for k1, v1 in v0['columns'].items():
		object_dict.update({k1: Column(
			eval(v1['dtype']),
			comment=v1['description'],
			primary_key=v1['primary_key'] if 'primary_key' in v1 else False)})
	vars()[k0]=type(k0, (Base, ), object_dict)


class tables(Base):
	"""
	Class for tracking metadata for tables in database.
	"""
	__table_args__={'schema' : 'metadata'}
	__tablename__='tables'
	

	schema_name=Column(String, comment='Schema name', primary_key=True)
	table_name=Column(String, comment='Table name', primary_key=True)
	description=Column(String, comment='table description')
	access_tier=Column(Integer, comment='Access control tier')
	pii=Column(Boolean, comment='Personally identifiable information flag')


class columns(Base):
	"""
	Class for tracking metadata for all columns in database.
	"""
	__table_args__={'schema' : 'metadata'}
	__tablename__='columns'
	

	schema_name=Column(String, comment='Schema name', primary_key=True)
	table_name=Column(String, comment='Table name', primary_key=True)
	column_name=Column(String, comment='Column name', primary_key=True)
	description=Column(String, comment='Column description')
	pii=Column(Boolean, comment='Personally identifiable information flag')


class trigger_functions(Base):
	"""
	Class for tracking metadata for all trigger_functions in database.
	"""
	__table_args__={'schema' : 'metadata'}
	__tablename__='trigger_functions'
	

	schema_name=Column(String, comment='Schema name', primary_key=True)
	trigger_function_name=Column(String, comment='Trigger function name', primary_key=True)
	source_tables=Column(ARRAY(String), comment='Source name')
	target_table=Column(String, comment='Target')
