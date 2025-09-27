.PHONY: up down dev

up:
	docker compose -f ops/docker-compose.yaml up --build

down:
	docker compose -f ops/docker-compose.yaml down -v

dev:
	uvicorn server.python_fastapi.app:app --reload
