import json
import logging

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(['GET', 'POST', 'DELETE'])
def cache_view(request, key):
    if request.method == 'GET':
        logger.info('Attempting to get from cache')
        value = cache.get(key)
        if value is None:
            return HttpResponseNotFound()
        return HttpResponse(value)
    elif request.method == 'POST':
        logger.info('Attempting to set into cache')
        request_json_data = json.loads(request.body)
        value = request_json_data.get('value')
        if value is None:
            return HttpResponseBadRequest()
        cache.set(key, value)
        return HttpResponse()
    elif request.method == 'DELETE':
        logger.info('Attempting to delete from cache')
        if cache.get(key) is None:
            return HttpResponseNotFound()
        cache.delete(key)
        return HttpResponse()
