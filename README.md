<h1 style='text-align: center;'>
𝔽𝕝𝕒𝕤𝕜-𝔹𝕒𝕤𝕖-𝔸ℙ𝕀
</h1>

## Overview

This project is a simple Flask API template that leverages Flask-RESTful for building RESTful APIs, Marshmallow for easy serialization/deserialization of data, and Flask-SQLAlchemy for interacting with a SQL database.

## Components

* Flask-RESTful: An extension for Flask that simplifies the creation of RESTful APIs. It allows you to define resources and easily map them to HTTP methods.

* Flask-SQLAlchemy: An extension for Flask that adds support for SQLAlchemy, an Object-Relational Mapping (ORM) library, making it easy to work with databases.

* Marshmallow: An integration of the Marshmallow library with Flask, providing a simple way to convert complex data types into JSON and back.

<div style='text-align: center;'>

[![Python](https://img.shields.io/static/v1?label=Python&message=v3.12.x&color=00CC11)](https://www.python.org/)
[![Flask](https://img.shields.io/static/v1?label=Flask&message=v3.0.2&color=00CC11)](https://flask.palletsprojects.com/en/3.0.x/)
[![Flask-SQLAlchemy](https://img.shields.io/static/v1?label=Flask-SQLAlchemy&message=v3.1.1&color=00CC11)](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
[![Flask-RESTful](https://img.shields.io/static/v1?label=Flask-RESTful&message=v0.3.10&color=00CC11)](https://flask-restful.readthedocs.io/en/latest/)
[![Marshmallow](https://img.shields.io/static/v1?label=Marshmallow&message=v3.20.2&color=00CC11)](https://marshmallow.readthedocs.io/en/stable/#)

</div>

## Installation using venv

Clone the repository:
```bash
git clone https://github.com/Leon047/flask_base_api.git
```
Install dependencies:
```bash
pip install --upgrade -r requirements.txt
```

Set environment variables:
```bash
source env
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
- [Flask_Base_API](http://127.0.0.1:8000/hello)
  
Expected output:
<pre>
{
  "api": "v1",
  "status": "success",
  "data": "Hello World"
}
</pre>
