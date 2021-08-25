"""
Load and parse config file.
"""


# Imports.
import yaml


# Read YAML file.
with open('src/config/config.yml', 'r') as stream:
    config=yaml.safe_load(stream)


# TODO: Add config validation.


# Extract some parameters into variables.
username=config['username']
password=config['password']
host=config['host']
port=5432
database=config['database']
schema='db'
objects=config['objects']
trigger_functions=config['trigger_functions']
secret_key=config['secret_key']
users=config['users']
