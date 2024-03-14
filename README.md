# Flask Base API

<div align='center'>

[![Python](https://img.shields.io/static/v1?label=Python&message=v3.12.x&color=00CC11)](https://www.python.org/)
[![Flask](https://img.shields.io/static/v1?label=Flask&message=v3.0.2&color=00CC11)](https://flask.palletsprojects.com/en/3.0.x/)
[![Flask-SQLAlchemy](https://img.shields.io/static/v1?label=Flask-SQLAlchemy&message=v3.1.1&color=00CC11)](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
[![Flask-RESTful](https://img.shields.io/static/v1?label=Flask-RESTful&message=v0.3.10&color=00CC11)](https://flask-restful.readthedocs.io/en/latest/)
[![Marshmallow](https://img.shields.io/static/v1?label=Marshmallow&message=v3.20.2&color=00CC11)](https://marshmallow.readthedocs.io/en/stable/#)

</div>

## Overview

This project is a simple Flask API template that leverages Flask-RESTful for building RESTful APIs, Marshmallow for easy serialization/deserialization of data, and Flask-SQLAlchemy for interacting with a SQL database.


## Components

* Flask-RESTful: An extension for Flask that simplifies the creation of RESTful APIs. It allows you to define resources and easily map them to HTTP methods.

* Flask-SQLAlchemy: An extension for Flask that adds support for SQLAlchemy, an Object-Relational Mapping (ORM) library, making it easy to work with databases.

* Marshmallow: An integration of the Marshmallow library with Flask, providing a simple way to convert complex data types into JSON and back.


## Getting Started

> Follow these steps to set up your Flask Base Api.

Clone the repository:
```bash
git clone https://github.com/Leon047/flask_base_api.git
```

Make changes to <code>.env</code> file:
<pre>
# ** General ** 
# App secret key (Change me!).
# Generate a key with 'secrets.token_hex(24)'.
export SECRET_KEY='2684b67b7067cdd17f6655c7a3e7e8fe3489e632f3449ab4'

# ** Database ** 
# Set the configuration parameter for connecting to the database.
# For example:(mysql://, postgresql://, sqlite://)
export SQLALCHEMY_DATABASE_URI='sqlite://'
</pre>

Basic configuration in the <code>config.py</code> file:
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


## Installation using venv

Install dependencies:
```bash
pip install --upgrade -r requirements.txt
```

Set environment variables:
```bash
source .env
```

Run the application:
```bash
python run.py
```


## Installation using Docker

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
|   ├── messages.py
|   ├── models.py
│   ├── schemas.py
|   ├── views.py
│   └── ...
|
├── tests/
│   └── ...
|
├── config.py
├── docker-compose.dev.yml
├── Dockerfile
├── .env
├── requirements.txt
├── run.py
</pre>


## License

This project is licensed under the MIT License
