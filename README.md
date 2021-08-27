# dataplatform-lite

**dataplatform-lite** is a framework and toolset for configuring and deploying lightweight data platforms and pipelines. It includes:
* a framework for creating data sets and dataflows within a PostgreSQL database
* automaticaly generated RESTful API endpoints to enable user access to data (using FastAPI)
* interactive data catalogues generated automatically from metadata
* interactive API documentation generated automatically from metadata
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

Go to [http://127.0.0.1:4141/](http://127.0.0.1:4141/) to access your interactive data catalogue.

Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access your interactive API documentation. The API is secured using OAuth2. Refer to the config.yml file to obtain credentials to authenticate and retrieve a bearer token.

## Running locally

## Configuring your own pipeline
