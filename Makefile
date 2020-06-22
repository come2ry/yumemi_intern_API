#!make
include .env
export $(shell sed 's/=.*//' .env)
c =

migrate:
	pipenv run alembic revision --autogenerate -m "$(m)"

upgrade:
	pipenv run alembic upgrade head

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
