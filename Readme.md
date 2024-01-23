# Connect

Welcome to Connect, a robuste API crafted with Django-Rest Framework that seamlessly integrates various features to enhance user experience.

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

The API incorporates Simple JWT for secure authentication, offering user registration and login endpoints along with a reliable token generation and refresh mechanism. Posts within Connect utilize the Taggit system to categorize posts and provide users with automatically discovered similar posts based on tags.

Connect also features a Redis-powered post view tracking system, ensuring efficient storage and retrieval of post views. This functionality is leveraged to showcase the most viewed posts prominently. Additionally, users can engage with posts through comments and likes, contributing to a dynamic and interactive platform.

The authorization system in Connect is strengthened with a custom authorization class, extending Django's BasePermission. This enables fine-grained control over access to resources, ensuring a secure environment.

To further enhance user interactions, Connect leverages the capabilities of Django Rest Framework, providing pagination for a seamless browsing experience. Users can filter posts based on various criteria, utilize a powerful search functionality, and order posts intuitively according to different fields.

## Technologies

- Python
- Django
- Postgresql
- Redis

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
