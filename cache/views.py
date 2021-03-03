from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import json

@csrf_exempt
@require_GET
def get(request, key):
    value = cache.get(key)
    if value is None:
        return HttpResponseNotFound()
    return HttpResponse(value)

@csrf_exempt
@require_POST
def set(request, key):
    request_json_data = json.loads(request.body)
    value = request_json_data.get('value')
    if value is None:
        return HttpResponseBadRequest()
    cache.set(key, value)
    return HttpResponse()

@csrf_exempt
@require_http_methods(['DELETE'])
def delete(request, key):
    if cache.get(key) is None:
        return HttpResponseNotFound()
    cache.delete(key)
    return HttpResponse()
