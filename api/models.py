import uuid

from django.db import models

class Set(models.Model):
    uuid = models.UUIDField(db_column='id', primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def get_elements(self):
        return Element.objects.filter(set=self)

class Element(models.Model):
    uuid = models.UUIDField(db_column='id', primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    set = models.ForeignKey('Set', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    