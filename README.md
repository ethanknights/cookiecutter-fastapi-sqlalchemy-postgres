# Cookiecutter Sample: FastAPI, SQLAlchemy & Postgres
A FastAPI application template (https://fastapi.tiangolo.com/tutorial/sql-databases/) amended with a postgres backend.

# Quickstart
Start FastAPI server: `uvicorn src.main:app --reload`

# First time setup
If using fresh postgres docker image, remember to setup create a database matching that in `database.py`'s `SQLALCHEMY_DATABASE_URL`: 

```
ethanknights % docker exec -it postgres-cookiecutter psql -U postgres -d postgres
postgres=# CREATE DATABASE cookiecutter;
```