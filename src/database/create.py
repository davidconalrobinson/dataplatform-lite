"""
Create database.
"""


# Imports.
import time
from src.database.base import *
from src.database.objects import *
from src.helpers.helpers import sequence_in
from src.config.config_loader import schema, trigger_functions, objects


def before_create(Base, schema):
	"""
	Steps before creating database:
		- create schema
		- enable uuid extension
	"""
	def before_create(target, connection, **kwargs):
		sql=text("""
			CREATE SCHEMA IF NOT EXISTS {schema};
			CREATE SCHEMA IF NOT EXISTS metadata;
			CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
			""".format(schema=schema))
		connection.execute(sql)
	event.listen(Base.metadata, 'before_create', before_create)


def after_create(Base, schema, objects, trigger_functions=[]):
	"""
	Create functions after creating database.
	"""
	def after_create(target, connection, **kwargs):
		sql=[]
		if objects:
			for table_name, table_metadata in objects.items():
				table_pii=False
				for column_name, column_metadata in table_metadata['columns'].items():
					# Set table_pii to true if any column contains pii
					table_pii=True if column_metadata['pii'] else table_pii
					# Insert column metadata.
					sql+=["""
						INSERT INTO metadata.columns (schema_name, table_name, column_name, description, pii)
						VALUES ('{}', '{}', '{}', '{}', {});
						""".format(schema, table_name, column_name, column_metadata['description'], column_metadata['pii'])]
				# Insert table metadata.
				sql+=["""
					INSERT INTO metadata.tables (schema_name, table_name, description, access_tier, pii)
					VALUES ('{}', '{}', '{}', {}, {});
					""".format(schema, table_name, table_metadata['description'], table_metadata['access_tier'], table_pii)]
		if trigger_functions:
			sql+=trigger_functions
			for trigger_function in trigger_functions:
				# Convert sql query to list.
				trigger_function_list=trigger_function.split()
				# Find trigger function name.
				trigger_function_name=trigger_function_list[sequence_in(trigger_function_list, ['CREATE', 'OR', 'REPLACE', 'FUNCTION'], offset=4)[0]]
				# Find source tables.
				source_tables=[]
				source_tables+=[trigger_function_list[i] for i in sequence_in(trigger_function_list, ['AFTER', 'INSERT', 'ON'], offset=3)]
				source_tables+=[trigger_function_list[i] for i in sequence_in(trigger_function_list, ['INNER', 'JOIN'], offset=2)]
				# Find target table.
				target_table=trigger_function_list[sequence_in(trigger_function_list, ['INSERT', 'INTO'], offset=2)[0]]
				# Insert trigger function metadata.
				sql+=["""
					INSERT INTO metadata.trigger_functions (schema_name, trigger_function_name, source_tables, target_table)
					VALUES ('{}', '{}', '{}', '{}');
					""".format(schema, trigger_function_name, '{\"'+'\", \"'.join(source_tables)+'\"}', target_table)]
		if sql:
			connection.execute(text(''.join(set(sql))))
	event.listen(Base.metadata, 'after_create', after_create)


def create_all(Base, schema, engine):
	"""
	Create schema and database.
	"""
	before_create(Base, schema)
	after_create(Base, schema, objects, trigger_functions=trigger_functions)
	Base.metadata.create_all(engine)


if __name__ == '__main__':
	while True:
		try:
			# Ping connection.
			with engine.connect() as connection:
				result=connection.execute('SELECT True AS ping')
				for row in result:
					ping=row['ping']
			break
		except Exception as e:
			print(e)
			print('waiting for infra before deploying db src code', flush=True)
			time.sleep(10)
	if ping:
		create_all(Base, schema, engine)
		print('db src code deployed', flush=True)
