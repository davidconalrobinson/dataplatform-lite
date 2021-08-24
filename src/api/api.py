"""
Define RESTful API for interfacing with dataplatform using fastapi.
"""


# Imports.
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.config.config_loader import objects
from src.database.base import engine
from src.database.objects import *


# Loop through objects and generate a class for each.
for k0, v0 in objects.items():
	param_object_dict={}
	body_object_dict={}
	for k1, v1 in v0['columns'].items():
		primary_key=v1['primary_key'] if 'primary_key' in v1 else False
		if primary_key:
			param_object_dict.update({k1: v1['dtype']})
		else:
			body_object_dict.update({k1: v1['dtype']})
	vars()['params_{}'.format(k0)]=type('params_{}'.format(k0), (BaseModel, ), param_object_dict)
	vars()['body_{}'.format(k0)]=type('body_{}'.format(k0), (BaseModel, ), body_object_dict)


# Create fastapi app.
app=FastAPI()


def create_post(table, columns_primary, columns):
	"""
	Create post endpoint programmatically (for data ingestion).
	"""
	@app.post('/{}/'.format(table))
	def ingest(body: eval('body_{}'.format(table)), params: eval('params_{}'.format(table))=Depends()):
		body_dict={}
		for column in columns_primary:
			body_dict.update({column: getattr(params, column)})
		for column in columns:
			body_dict.update({column: getattr(body, column)})
		session=Session(engine)
		session.add(eval(table)(**body_dict))
		session.commit()
		session.close()
		return(body)


def create_get(table, columns_primary, columns):
	"""
	Create get endpoint programmatically (for data consumption).
	"""
	@app.get('/{}/'.format(table))
	def consume(params: eval('params_{}'.format(table))=Depends()):
		filter={}
		for column in columns_primary:
			filter.update({column: getattr(params, column)})
		session=Session(engine)
		result=session.query(eval(table)).filter_by(**filter).all()[0]
		session.close()
		result_dict={}
		for column in columns_primary+columns:
			result_dict.update({column: getattr(result, column)})
		return(result_dict)


# Loop through tables and columns to create endpoints.
for k0, v0 in objects.items():
	table=k0
	columns=[]
	columns_primary=[]
	for k1, v1 in v0['columns'].items():
		primary_key=v1['primary_key'] if 'primary_key' in v1 else False
		if primary_key:
			columns_primary+=[k1]
		else:
			columns+=[k1]
	if 'get' in v0['api']:
		create_get(table, columns_primary, columns)
	if 'post' in v0['api']:
		create_post(table, columns_primary, columns)
