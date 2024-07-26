start:
	uvicorn app.main:app --reload

msg := ""
revision:
	alembic revision --autogenerate -m "$(msg)"

migrate:
	alembic upgrade head

infras:
	docker compose -f infrastructure.yml up -d

downv:
	docker compose -f infrastructure.yml down -v