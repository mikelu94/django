from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def produce(request):
    logger.info('Attempting to publish to Kafka')
    try:
        producer = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVERS)
        json.loads(request.body)
        producer.send(settings.KAFKA_TOPIC, request.body)
        return HttpResponse()
    except json.decoder.JSONDecodeError:
        return HttpResponseBadRequest('Request Body needs to be in JSON format')
    except NoBrokersAvailable:
        return HttpResponse('Kafka Broker is unavailable', status=503)
