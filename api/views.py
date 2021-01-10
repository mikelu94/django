from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Set, Element

class RestView(View):
    model = None

    def load_request_json_data(self, request):
        return json.loads(request.body)

    def get(self, request, uuid=None):
        if uuid is None:
            model_objects = [str(model_object.__dict__) for model_object in self.model.objects.all().iterator()]
            return HttpResponse(f'[{", ".join(model_objects)}]')
        try:
            return HttpResponse(str(self.model.objects.get(uuid=uuid).__dict__))
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

    def post(self, request, uuid=None):
        if uuid is not None:
            return HttpResponseNotFound()
        try:
            request_json_data = self.load_request_json_data(request)
            self.model.objects.create(**request_json_data)
            return HttpResponse()
        except Exception:
            return HttpResponseBadRequest()

    def put(self, request, uuid=None):
        if uuid is None or not self.model.objects.filter(uuid=uuid).exists():
            return HttpResponseNotFound()
        try:
            request_json_data = self.load_request_json_data(request)
            for field in self.model._meta.fields:
                if field.name not in request_json_data:
                    request_json_data[field.name] = None
            self.model.objects.filter(uuid=uuid).update(**request_json_data)
            return HttpResponse()
        except Exception:
            return HttpResponseBadRequest()
        
    def patch(self, request, uuid=None):
        if uuid is None or not self.model.objects.filter(uuid=uuid).exists():
            return HttpResponseNotFound()
        try:
            request_json_data = self.load_request_json_data(request)
            self.model.objects.filter(uuid=uuid).update(**request_json_data)
            return HttpResponse()
        except Exception:
            return HttpResponseBadRequest()

    def delete(self, request, uuid=None):
        if uuid is None or not self.model.objects.filter(uuid=uuid).exists():
            return HttpResponseNotFound()
        self.model.objects.get(uuid=uuid).delete()
        return HttpResponse() 

@method_decorator(csrf_exempt, name='dispatch')
class SetView(RestView):
    model = Set

@method_decorator(csrf_exempt, name='dispatch')
class ElementView(RestView):
    model = Element
    def load_request_json_data(self, request):
        request_json_data = json.loads(request.body)
        request_json_data['set'] = Set.objects.get(uuid=request_json_data['set_uuid'])
        del request_json_data['set_uuid']
        return request_json_data

@csrf_exempt
@require_GET
def cache_get(request, key):
    value = cache.get(key)
    if value is None:
        return HttpResponseNotFound()
    return HttpResponse(value)

@csrf_exempt
@require_POST
def cache_set(request, key):
    request_json_data = json.loads(request.body)
    value = request_json_data.get('value')
    if value is None:
        return HttpResponseBadRequest()
    cache.set(key, value)
    return HttpResponse()

@csrf_exempt
@require_http_methods(['DELETE'])
def cache_delete(request, key):
    if cache.get(key) is None:
        return HttpResponseNotFound()
    cache.delete(key)
    return HttpResponse()
