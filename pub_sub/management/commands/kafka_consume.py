import json
import logging
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Kafka Consumer'

    def handle(self, *args, **options):
        while True:
            try:
                consumer = KafkaConsumer(
                    settings.KAFKA_TOPIC,
                    group_id=settings.KAFKA_CONSUMER_GROUP_ID,
                    bootstrap_servers=settings.KAFKA_SERVERS,
                    value_deserializer=lambda m: json.loads(m.decode())
                )
                for message in consumer:
                    logger.info('Attempting to consume from Kafka')
                    logger.info(message.value)
            except NoBrokersAvailable:
                logger.info('No Brokers are available, attemping again in 60 seconds.')
                time.sleep(60)
