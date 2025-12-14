import json
from datetime import datetime
import time
from kafka import KafkaConsumer


class KafkaExtractor:

    def __init__(self, consumer: KafkaConsumer, batch_size: int = 1):
        self.consumer = consumer
        self.batch_size = batch_size
        self.batch_timeout = 10  # 1 минута

    def extract(self):
        """Собирает сообщения из Kafka в батч."""
        batch = []
        last_flush_time = time.time()

        for message in self.consumer:
            message_data = self.prepare_data(message.value)
            batch.append(message_data)

            current_time = time.time()

            # Отправляем если:
            # 1. Батч достиг размера
            # 2. Прошла минута и в батче есть данные
            if (len(batch) >= self.batch_size or
                    (len(batch) > 0 and current_time - last_flush_time >= self.batch_timeout)):
                yield batch
                batch = []
                last_flush_time = current_time

    def prepare_data(self, message: bytes) -> tuple:
        """Конвертирует сообщение в словарь."""
        message_dict = json.loads(message.decode("utf-8"))
        message_dict["event_time"] = datetime.strptime(
            message_dict["event_time"], "%Y-%m-%d %H:%M:%S"
        )
        return message_dict