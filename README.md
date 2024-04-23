# Flask Base API

<div align='center'>

[![Python](https://img.shields.io/static/v1?label=Python&message=v3.10.x&color=00CC11)](https://www.python.org/)
[![Flask](https://img.shields.io/static/v1?label=Flask&message=v3.0.2&color=00CC11)](https://flask.palletsprojects.com/en/3.0.x/)
[![Flask-SQLAlchemy](https://img.shields.io/static/v1?label=Flask-SQLAlchemy&message=v3.1.1&color=00CC11)](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
[![Flask-RESTful](https://img.shields.io/static/v1?label=Flask-RESTful&message=v0.3.10&color=00CC11)](https://flask-restful.readthedocs.io/en/latest/)
[![Flask-Alembic](https://img.shields.io/static/v1?label=Flask-Alembic&message=v3.0.1&color=00CC11)](https://flask-alembic.readthedocs.io/en/latest/#)
[![Marshmallow](https://img.shields.io/static/v1?label=Marshmallow&message=v3.20.2&color=00CC11)](https://marshmallow.readthedocs.io/en/stable/#)

</div>

## Overview

This project is a simple Flask API template that leverages Flask-RESTful for building RESTful APIs, Marshmallow for easy serialization/deserialization of data, Flask-SQLAlchemy for interacting with a SQL database and Flask-Alembic for database schema migrations.


## Components

* Flask-RESTful: An extension for Flask that simplifies the creation of RESTful APIs. It allows you to define resources and easily map them to HTTP methods.

* Flask-SQLAlchemy: An extension for Flask that adds support for SQLAlchemy, an Object-Relational Mapping (ORM) library, making it easy to work with databases.

* Flask-Alembic: Integrates the Alembic migration framework with Flask, enabling automated database schema migrations and version control within Flask applications. 

* Marshmallow: An integration of the Marshmallow library with Flask, providing a simple way to convert complex data types into JSON and back.


## Functionality: CRUD API for Basic User Authentication

This project includes a CRUD API to manage basic user authentication. The API provides endpoints to perform CRUD operations on user records, including managing usernames, passwords, and authentication.

The CRUD API includes the following endpoints:

USER API:
- `GET /api/v1/user`
- `PUT /api/v1/user`
- `PATCH /api/v1/user`
- `DELETE /api/v1/user`

PASSWORD API:
- `POST /api/v1/user/password`

AUTH API:
- `POST /api/v1/user/auth`
- `DELETE /api/v1/user/auth`

The API supports basic user authentication using username and password.


## 🚀 Getting Started

> Follow these steps to set up your Flask Base Api.

Clone the repository:
```bash
git clone https://github.com/Leon047/flask_base_api.git
```

Make changes to the `.env` file:
<pre>
  # ** General ** 
  # App secret key (Change me!).
  # Generate a key with 'secrets.token_hex(24)'.
  export SECRET_KEY='2684b67b7067cdd17f6655c7a3e7e8fe3489e632f3449ab4'
  
  # ** Database ** 
  # Set the configuration parameter for connecting to the database.
  # For example:(mysql://, postgresql://, sqlite://)
  export SQLALCHEMY_DATABASE_URI='sqlite:///sqlite_database.db'
</pre>

Basic configuration in the `config.py` file:
<pre>
  class Config:
      """
      Set Flask configuration.
      """
      # General Config
      SECRET_KEY = os.environ.get('SECRET_KEY')
      DEBUG = True    # Only for debugging while developing
      HOST = '0.0.0.0'
      PORT = 8000
  
      # Database
      SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
      SQLALCHEMY_ECHO = False
      SQLALCHEMY_TRACK_MODIFICATIONS = False
</pre>

Basic configuration in the `alembic.ini` file:
<pre>
  # sqlalchemy.url
  sqlalchemy.url = sqlite:///sqlite_database.db
</pre>


## Installation using venv

Install dependencies:
```bash
pip install --upgrade -r requirements.txt
```

Set environment variables:
```bash
source .env
```

Initialization Alembic:
```bash
alembic init alembic
```

Generating the first migration:
```bash
alembic revision -m 'Initial migration'
```

Applying Migrations:
```bash
alembic upgrade head
```

Run the application:
```bash
python run.py
```


## Installation using Docker
Docker Compose includes a configuration for Flask without a database. Choose a suitable version of the database and supplement it considering `Flask-Alembic`.

Dockerfile:
<pre>
  FROM python:3.10
  WORKDIR /back
  COPY . /back
  RUN apt-get update -y &&\
    pip install --upgrade pip &&\
    pip install --no-cache -r requirements.txt
</pre>

docker-compose.dev.yml:
<pre>
  version: '3'
  services:
  
    back:
      build: 
        context: .
        dockerfile: Dockerfile
      volumes:
        - .:/back
      container_name: back_dev
      ports:
        - '8000:8000'
      command: python run.py
      environment:
        SECRET_KEY: $SECRET_KEY
        SQLALCHEMY_DATABASE_URI: $SQLALCHEMY_DATABASE_URI
</pre>

Set environment variables:
```bash
source .env
```

Build and run the Docker Compose services:
```bash
docker-compose -f docker-compose.dev.yml up --build
```


## Start

The project will start:
- http://0.0.0.0:8000/api/v1/hello 
  
Expected output:
<pre>
  {
    "api": "v1",
    "status": "success",
    "data": "Hello World"
  }
</pre>


## Project Structure

<pre>
  flask_base_api/
  │
  ├── src/
  │   ├── __init__.py
  │   ├── messages.py
  │   ├── models.py
  │   ├── schemas.py
  │   ├── utils.py 
  │   ├── views.py
  │   └── ...
  │ 
  ├── tests/
  │   ├── __init__.py
  │   ├── conftest.py 
  │   ├── /test_routs
  │   ├── /test_schemas
  │   └── ...
  │ 
  ├── alembic.ini 
  ├── config.py
  ├── docker-compose.dev.yml
  ├── Dockerfile
  ├── .dockerignore 
  ├── .env
  ├── error.log
  ├── .gitignore 
  ├── LICENSE
  ├── README.md 
  ├── requirements.txt
  ├── run.py
  └── sqlite_database.db 
</pre>


## Tests

In the project directory, after activating the `virtual environment`:

Set environment variables:
```bash
source .env
```

Run tests.
```bash
pytest
```


## License

This project is licensed under the MIT License
