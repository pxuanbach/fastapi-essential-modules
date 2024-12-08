start:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

msg := .
revision:
	alembic revision --autogenerate -m "$(msg)" 

infras:
	docker compose -f infrastructure.yaml up -d

install:
	poetry install

create-jobdb:
	docker compose -f infrastructure.yaml exec postgres createdb job_db -U postgres

create-testdb:
	docker compose -f infrastructure.yaml exec postgres createdb test_app -U postgres

reset-db:
	docker compose -f infrastructure.yaml down postgres -v
	docker compose -f infrastructure.yaml up postgres -d
	echo "sleep 5s"
	timeout 5
	$(MAKE) create-jobdb
	$(MAKE) create-testdb

test:
	pytest tests/models
