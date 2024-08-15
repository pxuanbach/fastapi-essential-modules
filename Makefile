start:
	uvicorn app.main:app --reload

infras:
	docker compose -f infrastructure.yaml up -d

install:
	poetry install
	