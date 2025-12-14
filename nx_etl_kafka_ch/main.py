from time import sleep

from configs.constants import settings
from configs.logger_config import logger
from related.ch_loader import ClickHouseLoader
from related.kafka_extractor import KafkaExtractor
from utils.ch_queries import queries_by_topic, params_by_topic
from utils.waiters import clickhouse_client_create, kafka_consumer_create


def start_etl_process():
    sleep_time_etl: int = 600
    query: str = queries_by_topic.get(settings.TOPIC)
    columns = params_by_topic.get(settings.TOPIC)
    consumer = kafka_consumer_create()

    extractor: KafkaExtractor = KafkaExtractor(consumer=consumer)
    loader: ClickHouseLoader = ClickHouseLoader(client=clickhouse_client_create())

    while True:
        logger.info("Collecting data from Kafka...")

        for batch in extractor.extract():
            print(batch)
            rows = [tuple(item[col] for col in columns) for item in batch]
            logger.info("Loading data to ClickHouse... " + str(batch))
            loader.load_data(batch=rows, query=query)
            consumer.commit()

        logger.info("Data loaded. I'm going to sleep for %s seconds.", sleep_time_etl)
        sleep(sleep_time_etl)


if __name__ == "__main__":
    logger.info("ETL process starting...")
    start_etl_process()
