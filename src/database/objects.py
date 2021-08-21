"""
Creates a python class for each of the objects defined in config file.

Each class maps to a database table using SQL alchemy ORM.
"""


# Imports.
from sqlalchemy import *
from src.database.base import Base
from src.config_loader import schema, objects


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
			comment=v1['comment'],
			primary_key=v1['primary_key'] if 'primary_key' in v1 else False)})
	vars()[k0]=type(k0, (Base, ), object_dict)
