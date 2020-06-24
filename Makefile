#!make
include .env
export $(shell sed 's/=.*//' .env)
c =

migrate:
	pipenv run alembic revision --autogenerate -m "$(m)"

upgrade:
	pipenv run alembic upgrade head

downgrade:
	pipenv run alembic downgrade -1

run:
	pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

init:
	pipenv run python app/init_data.py

db:
	mysql -u root -proot -h 127.0.0.1 -P 3306 yumemi_db;