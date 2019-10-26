import pika
import json


class PhotoProcessingQueue():
    def __init__(self, amqp_uri, queue_name):
        self._amqp_uri = amqp_uri
        self._queue_name = queue_name
        self._connection = None

    def _create_connection_and_channel(self):
        if self._connection:
            return

        parameters = pika.URLParameters(self._amqp_uri)
        self._connection = pika.BlockingConnection(parameters)

        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name, durable=True)

    def _process_message(self, ch, method, properties, body):
        uuid = None

        try:
            uuid = json.loads(body)['photo_uuid']
        except Exception as e:
            logger.error('Failed to obtain uuid of the photo from the mq message')
            logger.exception(f'Exception: {e}')
            ch.basic_nack(delivery_tag = method.delivery_tag, requeue=False)
            return

        if self._processing_handler(uuid):
            ch.basic_ack(delivery_tag = method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag = method.delivery_tag, requeue=False)

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def submit_photo(self, uuid):
        self._create_connection_and_channel()

        message = json.dumps({'photo_uuid': uuid})

        self._channel.basic_publish(
            exchange='',
            routing_key=self._queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2
            ))

    def process_photos(self, processing_handler):
        self._create_connection_and_channel()

        self._processing_handler = processing_handler
        self._channel.basic_consume(queue=self._queue_name, on_message_callback=self._process_message)
        self._channel.start_consuming()

