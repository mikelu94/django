from django.db.models.fields import SlugField
from rest_framework import serializers

from .models import Element, Set


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['uuid', 'name']


class ElementSerializer(serializers.ModelSerializer):
    set = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Set.objects.all(),
        many=False,
    )
    
    class Meta:
        model = Element
        fields = ['uuid', 'name', 'set']
    
