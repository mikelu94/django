import json
import logging

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class CacheView(APIView):
    def get(self, request, key, format=None):
        logger.info('Attempting to get from cache')
        value = cache.get(key)
        if value is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(value)

    def post(self, request, key, format=None):
        logger.info('Attempting to set into cache')
        value = request.data.get('value')
        if value is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cache.set(key, value)
        return Response()

    def delete(self, request, key, format=None):
        logger.info('Attempting to delete from cache')
        if cache.get(key) is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cache.delete(key)
        return Response()
