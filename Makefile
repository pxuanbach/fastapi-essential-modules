start:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

infras:
	docker compose -f infrastructure.yaml up -d

install:
	poetry install

create-jobdb:
	docker compose -f infrastructure.yaml exec postgres createdb job_db -U postgres

monitor:
	docker compose -f ./monitoring/docker-compose.yaml up -d
