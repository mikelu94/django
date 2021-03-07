from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
import json
import logging

from .models import Set, Element

logger = logging.getLogger(__name__)


class RestView(View):
    model = None

    def load_request_json_data(self, request):
        return json.loads(request.body)

    def get(self, request, uuid=None):
        if uuid is None:
            model_objects = [str(model_object.__dict__) for model_object in self.model.objects.all().iterator()]
            logger.info(f'Reading all {self.model.__name__} objects')
            return HttpResponse(f'[{", ".join(model_objects)}]')
        try:
            logger.info(f'Attempting to read {self.model.__name__} object')
            return HttpResponse(str(self.model.objects.get(uuid=uuid).__dict__))
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

    def post(self, request, uuid=None):
        if uuid is not None:
            return HttpResponseNotFound()
        try:
            logger.info(f'Attempting to create new {self.model.__name__} object')
            request_json_data = self.load_request_json_data(request)
            self.model.objects.create(**request_json_data)
            return HttpResponse()
        except Exception:
            return HttpResponseBadRequest()

    def put(self, request, uuid=None):
        if uuid is None or not self.model.objects.filter(uuid=uuid).exists():
            return HttpResponseNotFound()
        try:
            logger.info(f'Attempting to overwrite existing {self.model.__name__} object')
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
            logger.info(f'Attempting to modify existing {self.model.__name__} object')
            request_json_data = self.load_request_json_data(request)
            self.model.objects.filter(uuid=uuid).update(**request_json_data)
            return HttpResponse()
        except Exception:
            return HttpResponseBadRequest()

    def delete(self, request, uuid=None):
        if uuid is None or not self.model.objects.filter(uuid=uuid).exists():
            return HttpResponseNotFound()
        logger.info(f'Attempting to delete {self.model.__name__} object')
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
