import json
import logging

from django.conf import settings
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(['POST'])
def produce(request):
    logger.info('Attempting to publish to Kafka')
    try:
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_SERVERS,
            value_serializer=lambda d: json.dumps(d).encode()
        )
        producer.send(settings.KAFKA_TOPIC, request.data)
        return Response()
    except NoBrokersAvailable:
        return Response('Kafka Broker is unavailable', status=status.HTTP_503_SERVICE_UNAVAILABLE)
