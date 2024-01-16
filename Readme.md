# Connect

## Table of Contents

- [Prerequisites](#Prerequisites)
- [Getting Started](#getting-started)
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Usage](#usage)

## Prerequisites

Before you dive in, make sure you have the following requirements in place:

- [Python](https://www.python.org/)
- [Pipenv](https://pipenv.pypa.io/)
- [Postgresql](https://www.postgresql.org/)
- [Redis](https://redis.io/)

Install the necessary Python packages within a virtual environment using the following command:

```
pipenv install
```

## Getting-started

- Access the PostgreSQL shell and create a database and user for the application using the following commands:

```psql
create database mydb;
create user myuser with encrypted password 'mypass';
grant all privileges on database mydb to myuser;
```

- Add the configurations to the **'.env'** file in the project's root.<br>

```conf
DEBUG=on
SECRET_KEY='django-project-secret-key'
DATABASE_URL=psql://myuser:mypass@localhost:5432/mydb
REDIS_URL=redis://127.0.0.1:6379
```

- Apply migrations to the database:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

- Run Redis Server:

```bash
redis-server
```

## Introduction

## Technologies

- Python
- Django
- Postgresql

## Usage

- Ensure that migrations are applied to the database:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

- Ensure that Redis server is running:

```bash
redis-server
```

- Start by running:

```bash
python3 manage.py runserver
```
