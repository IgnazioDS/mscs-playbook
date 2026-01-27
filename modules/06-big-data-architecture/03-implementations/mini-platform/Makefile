COMPOSE_FILE=modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml

up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down -v

demo:
	bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/demo.sh
