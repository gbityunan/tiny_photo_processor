export PG_USERNAME=tpp
export PG_PASSWORD=1234
export PG_DATABASE=tpp
export PG_CONNECTION_URI=postgres://$(PG_USERNAME):$(PG_PASSWORD)@postgres/$(PG_DATABASE)

export AMQP_USERNAME=rabbitmq
export AMQP_PASSWORD=1234
export AMQP_URI=amqp://$(AMQP_USERNAME):$(AMQP_PASSWORD)@rabbitmq:5672/%2f

start:
	docker-compose up --build

restart-app:
	docker-compose up -d --no-deps --build app

create-db:
	docker exec -it tpp-app alembic upgrade head

revise-db:
	docker exec -it tpp-app alembic revision --autogenerate

upgrade-db:
	docker exec -it tpp-app alembic upgrade head

downgrade-db:
	docker exec -it tpp-app alembic downgrade -1

psql:
	docker exec -it postgres psql $(PG_CONNECTION_URI)

shell:
	docker exec -it tpp-app /bin/ash
