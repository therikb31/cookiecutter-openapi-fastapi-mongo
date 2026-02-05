.PHONY: dev docker-build docker-compose-up docker-compose-down

dev:
	@docker run -itd --rm \
		--name mongodb \
		-p 27017:27017 \
		-e MONGO_INITDB_ROOT_USERNAME={{ cookiecutter.mongo_username }} \
		-e MONGO_INITDB_ROOT_PASSWORD={{ cookiecutter.mongo_password }} \
		-e MONGO_INITDB_DATABASE={{ cookiecutter.mongodb_name }} \
		mongo:7.0
	@uv run services/{{ cookiecutter.service_name }}/main.py

docker-build:
	@docker build -t {{ cookiecutter.project_dir_name }}:latest .

docker-compose-up:
	@docker-compose up -d --build

docker-compose-down:
	@docker-compose down -v
