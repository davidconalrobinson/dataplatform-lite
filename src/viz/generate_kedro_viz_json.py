"""
Opens a visualisation of the data pipeline using kedro-viz.
"""


# Imports.
import json
import pandas as pd
from src.database.base import engine


def get_tables(engine):
	"""
	Get the tables in the data pipeline.
	"""
	sql="""
		SELECT
			*
		FROM metadata.tables
	"""
	return pd.read_sql(sql, engine)


def get_trigger_functions(engine):
	"""
	Get trigger functions in data pipeline.
	"""
	sql="""
		SELECT
			*
		FROM metadata.trigger_functions
	"""
	return pd.read_sql(sql, engine)


def generate_kedro_viz_dict(engine):
	"""
	Generate dict to pass to kedro-viz.
	"""
	tables=get_tables(engine)
	tables['fq_table']=tables['schema_name']+'.'+tables['table_name']
	trigger_functions=get_trigger_functions(engine)
	# Create edges object.
	edges=[]
	for i, trigger_function in trigger_functions.iterrows():
		for source_table in trigger_function['source_tables']:
			edges+=[{'source': source_table, 'target': trigger_function['trigger_function_name']}]
		edges+=[{'source': trigger_function['trigger_function_name'], 'target': trigger_function['target_table']}]
	# Create layers object.
	layers=tables['schema_name'].unique().tolist()
	# Create modular pipelines object.
	modular_pipelines=[]
	# Create nodes object.
	nodes=[]
	for i, table in tables.iterrows():
		nodes+=[{
			'dataset_type': table['fq_table'],
			'full_name': table['fq_table'],
			'id': table['fq_table'],
			'layer': table['schema_name'],
			'modular_pipelines': [],
			'name': table['fq_table'],
			'pipelines': ['__default__'],
			'tags': ['pii'] if table['pii'] else [],
			'type': 'data'
		}]
	for i, trigger_function in trigger_functions.iterrows():
		nodes+=[{
			'full_name': trigger_function['trigger_function_name'],
			'id': trigger_function['trigger_function_name'],
			'modular_pipelines': [],
			'name': trigger_function['trigger_function_name'],
			'parameters': {},
			'pipelines': ['__default__'],
			'tags': [],
			'type': 'task'
		}]
	# Create pipelines object.
	pipelines=[{'id': '__default__', 'name': 'Default'}]
	# Create selected pipeline object.
	selected_pipeline='__default__'
	# Creates tags object.
	tags=[{'id': 'pii', 'name': 'Personally Identifiable Information'}]
	# Create kedro viz dict
	kedro_viz_dict={}
	for key in ['edges', 'layers', 'modular_pipelines', 'nodes', 'pipelines', 'selected_pipeline', 'tags']:
		kedro_viz_dict[key]=eval(key)
	return kedro_viz_dict


def export_kedro_viz_dict(engine):
	"""
	Export viz json to be loaded by kedro viz.
	"""
	with open('src/viz/viz.json', 'w') as file:
		json.dump(generate_kedro_viz_dict(engine), file)


if __name__ == '__main__':
	export_kedro_viz_dict(engine)
