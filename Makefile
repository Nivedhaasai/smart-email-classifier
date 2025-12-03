.PHONY: help build up down logs clean restart test prod-build prod-up

help:
	@echo "Email Detection - Docker Commands"
	@echo "==================================="
	@echo "Development Commands:"
	@echo "  make build       - Build all Docker images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View all logs"
	@echo "  make clean       - Remove containers, volumes, and images"
	@echo ""
	@echo "Production Commands:"
	@echo "  make prod-build  - Build production images"
	@echo "  make prod-up     - Start production services"
	@echo ""
	@echo "Service Commands:"
	@echo "  make backend-logs   - View backend logs"
	@echo "  make frontend-logs  - View frontend logs"
	@echo "  make nginx-logs     - View Nginx logs"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make health      - Check service health"
	@echo "  make test-api    - Test API endpoint"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

backend-logs:
	docker-compose logs -f backend

frontend-logs:
	docker-compose logs -f frontend

nginx-logs:
	docker-compose logs -f nginx

restart:
	docker-compose restart

clean:
	docker-compose down -v --rmi all

health:
	@echo "Checking backend health..."
	@curl -s http://localhost:8000/health | jq . || echo "Backend not responding"
	@echo "\nChecking Nginx health..."
	@curl -s http://localhost/health || echo "Nginx not responding"

test-api:
	@echo "Testing API endpoints..."
	@curl -s -X POST http://localhost:8000/predict \
		-H "Content-Type: application/json" \
		-d '{"text": "urgent invoice payment due"}' | jq .

ps:
	docker-compose ps

shell-backend:
	docker-compose exec backend /bin/bash

shell-frontend:
	docker-compose exec frontend /bin/sh

prod-build:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache

prod-up:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

stats:
	docker stats

prune:
	docker system prune -a --volumes -f

rebuild: clean build up

version:
	@echo "Docker version:"
	@docker --version
	@echo "Docker Compose version:"
	@docker-compose --version
