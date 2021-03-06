## ODD MSSQL adapter

ODD MSSQL adapter is used for extracting datasets info and metadata from Microsoft SQL Server. This adapter is implemetation of pull model (see more https://github.com/opendatadiscovery/opendatadiscovery-specification/blob/main/specification/specification.md#discovery-models). By default application gather data from MSSQL every minute, put it inside local cache and then ready to give it away by /entities API.

This service based on Python Flask and Connexion frameworks with APScheduler.

#### Data entities:
| Entity type | Entity source |
|:----------------:|:---------:|
|Dataset|Tables, Columns|
|Data Transformer (coming soon)|Views|

For more information about data entities see https://github.com/opendatadiscovery/opendatadiscovery-specification/blob/main/specification/specification.md#data-model-specification

## Quickstart
Application is ready to run out of the box by the docker-compose (see more https://docs.docker.com/compose/).
Strongly recommended to override next variables in docker-compose .env file:

```
ODBC_DATABASE=master
ODBC_USER=sa
ODBC_PASSWORD=odd-adapter-password-1
```

After docker-compose run successful, application is ready to accept connection on port :8080. 
For more information about variables see next section.

#### Config for Helm:
```
podSecurityContext:
  fsGroup: 65534
image:
  pullPolicy: Always
  repository: 436866023604.dkr.ecr.eu-central-1.amazonaws.com/odd-mssql-adapter
  tag: ci-655380
nameOverride: odd-mssql-adapter
labels:
  adapter: odd-mssql-adapter
config:
  envFrom:
  - configMapRef:
      name: odd-mssql-adapter
  env:
  - name: DEMO_GREETING
    value: "Hello from the environment"
  - name: DEMO_FAREWELL
    value: "Such a sweet sorrow"
```
More info about Helm config in https://github.com/opendatadiscovery/charts


## Environment
Adapter is ready to work out of box, but you probably will need to redefine some variables in compose .env file:

```Python
MSSQL_PID=Developer

ODBC_DRIVER="ODBC Driver 17 for SQL Server"
ODBC_HOST=odd-mssql-db #Host of your ODBC.
ODBC_PORT=1433 #Port of your ODBC.
ODBC_DATABASE=master #Name of your ODBC.
ODBC_USER=sa #Username of your ODBC.
ODBC_PASSWORD=odd-adapter-password-1 #Password of your ODBC.
```

## Requirements
- Python 3.8
- MS SQL Server 2019-latest
