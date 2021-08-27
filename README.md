# dataplatform-lite

**dataplatform-lite** is a framework and toolset for configuring and deploying lightweight data platforms and pipelines. It includes:

* standardised framework for creating data sets and dataflows within a [PostgreSQL](https://www.postgresql.org/) database using [yaml](https://yaml.org/)
* automatically generated RESTful API endpoints to enable user access to data using [FastAPI](https://fastapi.tiangolo.com/)
* interactive data catalogues generated automatically from metadata using [Kedro](https://github.com/quantumblacklabs/kedro-viz)
* interactive [Swagger](https://swagger.io/) and [ReDoc](https://github.com/Redocly/redoc) API documentation generated automatically from metadata
* user access controls enforced automatically from metadata
* fully containerised using [Docker](https://www.docker.com/)

## Getting started

Start by cloning this repository:

```
git clone https://github.com/davidconalrobinson/dataplatform-lite
```

Copy one of the example configurations from examples/\*/config.yml to src/config/config.yml.

Download and install [Docker](https://www.docker.com/products/docker-desktop). Then run the following to build the docker images, start containers and deploy the data platform:

```
docker-compose up
```

Go to [127.0.0.1:4141/](http://127.0.0.1:4141/) to access your interactive data catalogue.

Go to [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access your interactive API documentation. The API is secured using OAuth2. Refer to the config.yml file to obtain credentials to authenticate and retrieve a bearer token.

## Running locally

While I recommend running dataplatform-lite using Docker, you may choose to deploy your platform locally or to a remote PostgreSQL server. To do this, you will first need to download and install Python 3.8 and pip (simply downloading and installing [Anaconda](https://www.anaconda.com/products/individual) is the easiest way to do this).

First, install requirements:

```
pip install -r requirements.txt
```

Update the "username", "password", "host" and "database" parameters in src/config/config.yml to point to the PostgreSQL database of your choosing. Then run the following to deploy your platform to the PostgreSQL server:

```
python -m src.database.create
```

Run the following to start the Kedro data catalogue server:

```
python -m src.viz.generate_kedro_viz_json
python -m kedro viz --load-file src/viz/viz.json
```

Go to [127.0.0.1:4141/](http://127.0.0.1:4141/) to access your interactive data catalogue.

Run the following to start the API server:

```
uvicorn src.api.api:app --reload
```

Go to [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access your interactive API documentation.

## Configuring your own platform

To configure your own platform from scratch, simply edit the [src/config/config.yml](https://github.com/davidconalrobinson/dataplatform-lite/blob/main/src/config/config.yml). Some things to note:

* You will need to complete all fields marked by parenthises ("<\*>")
* Add as many users as you like
* Add as many database objects as you like
* Add as many trigger functions as you like
* All database objects must have a description and access level
* All columns must have a type, description and PII flag