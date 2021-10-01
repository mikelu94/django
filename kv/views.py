import json
import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class KVView(APIView):
    def get(self, request, key, format=None):
        logger.info('Attempting to get from Key-Value Store')
        value = settings.REDIS.get(key)
        if value is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(value)
    
    def post(self, request, key, format=None):
        logger.info('Attempting to set to Key-Value Store')
        value = request.data.get('value')
        if value is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        settings.REDIS.set(key, value)
        return Response()

    def delete(self, request, key, format=None):
        logger.info('Attempting to delete from Key-Value Store')
        if settings.REDIS.get(key) is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        settings.REDIS.delete(key)
        return Response()
