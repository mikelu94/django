from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(['GET', 'POST', 'DELETE'])
def kv_view(request, key):
    if request.method == 'GET':
        logger.info('Attempting to get from Key-Value Store')
        value = settings.REDIS.get(key)
        if value is None:
            return HttpResponseNotFound()
        return HttpResponse(value)
    elif request.method == 'POST':
        logger.info('Attempting to set to Key-Value Store')
        request_json_data = json.loads(request.body)
        value = request_json_data.get('value')
        if value is None:
            return HttpResponseBadRequest()
        settings.REDIS.set(key, value)
        return HttpResponse()
    elif request.method == 'DELETE':
        logger.info('Attempting to delete from Key-Value Store')
        if settings.REDIS.get(key) is None:
            return HttpResponseNotFound()
        settings.REDIS.delete(key)
        return HttpResponse()
