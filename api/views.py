import logging

from rest_framework import viewsets

from .models import Element, Set
from .serializers import ElementSerializer, SetSerializer

logger = logging.getLogger(__name__)


class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    permission_classes = []


class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    permission_classes = []
