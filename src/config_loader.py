"""
Load and parse config file.
"""


# Imports.
import yaml


# Read YAML file.
with open('config.yaml', 'r') as stream:
    config=yaml.safe_load(stream)


# TODO: Add config validation.


# Extract some parameters into variables.
username=config['username']
password=config['password']
host=config['host']
port=config['port']
database=config['database']
schema=config['schema']
objects=config['objects']
trigger_functions=config['trigger_functions']
