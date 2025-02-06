import logging
import time

import pika

log = logging.getLogger(__name__)

RMQ_HOST = "localhost"
RMQ_PORT = 5672
RMQ_USER = "guest"
RMQ_PASSWORD = "guest"
MQ_EXCHANGE = ""
MQ_ROUTING_KEY = "logs"


class RabbitMQ:
    """Оптимизированный пул соединений RabbitMQ с автоматическим восстановлением."""

    def __init__(
        self,
        host=RMQ_HOST,
        port=RMQ_PORT,
        user=RMQ_USER,
        password=RMQ_PASSWORD,
    ):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(user, password)
        self.connection = None
        self.channel = None
        self._connect()  # Автоматически создаём соединение при запуске

    def _connect(self):
        """Создаёт соединение и канал с RabbitMQ."""
        try:
            if self.connection and self.connection.is_open:
                return

            log.info("🔌 Подключение к RabbitMQ...")

            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=self.credentials,
                    heartbeat=60,  # Поддержка соединения
                    blocked_connection_timeout=300,  # Увеличенный таймаут
                )
            )
            self.channel = self.connection.channel()
            self.channel.confirm_delivery()  # Включаем подтверждение доставки
            log.info("✅ Успешное подключение к RabbitMQ.")

        except Exception as e:
            log.error(f"❌ Ошибка соединения с RabbitMQ: {e}")
            time.sleep(5)
            self._connect()  # Рекурсивная попытка подключения

    def publish(self, queue, message):
        """Отправляет сообщение в очередь с проверкой успешности."""
        self._connect()  # Убедимся, что соединение активно

        try:
            self.channel.queue_declare(queue=queue, durable=True)
            message_body = message.encode("utf-8")
            self.channel.basic_publish(
                exchange=MQ_EXCHANGE,
                routing_key=queue,
                body=message_body,
            )

            log.info(f"📨 Сообщение отправлено в очередь {queue}")
            return True

        except Exception:
            log.error(f"⚠️ Сообщение не может быть доставлено в {queue} (unroutable).")
            return False

        # except pika.exceptions.AMQPConnectionError as e:
        #     log.error(f"❌ Ошибка при отправке сообщения: {e}")
        #     time.sleep(5)
        #     self._connect()  # Переподключаемся и пробуем снова
        #     return self.publish(queue, message)

    def close(self):
        """Закрывает соединение с RabbitMQ."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            log.info("🔌 Соединение с RabbitMQ закрыто.")


rabbitmq = RabbitMQ()
