up_kafka:
	docker-compose -f docker-compose.kafka.yaml up -d

down_kafka:
	docker-compose -f docker-compose.kafka.yaml down -v

up_clickhouse:
	docker-compose -f docker-compose.clickhouse.yaml up -d

down_clickhouse:
	docker-compose -f docker-compose.kafka.yaml down -v

up_services:
	docker-compose up -d

down_services:
	docker-compose down -v